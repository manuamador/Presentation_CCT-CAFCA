const c = 299792458.0
include("ADTest.jl")
tic()
function Efarfield(R,theta,phi,I,f)
	X=R*cos(phi)*sin(theta)
    Y=R*sin(phi)*sin(theta)
    Z=R*cos(theta)
	DX = X-I[1]
	DY = Y-I[2]
	DZ = Z-I[3]
	dist = sqrt(DX^2+DY^2+DZ^2)
	phase=2*pi*dist*f/c+I[7]
	ca    = cos(I[4])
	sa    = sin(I[4])
	cb    = cos(I[5])
	sb    = sin(I[5])
	distx = ((-sb)^2+(1-(-sb)^2)*ca)*DX+(-sb*cb*(1-ca))*DY+(cb*sa)*DZ
	disty = (-sb*cb*(1-ca))*DX+((cb)^2+(1-cb^2)*ca)*DY+(sb*sa)*DZ
	distz = (-cb*sa)*DX+(-sb*sa)*DY+ca*DZ
	distxy = sqrt(distx^2+disty^2)
	costheta = distz/dist
	sintheta = distxy/dist
	cosphi   = distx/distxy
	sinphi   = disty/distxy
	L =I[6]*1/dist*(f/c)^2*377
	Exx = exp(1im*phase)*L*((((-sb)^2+(1-(-sb)^2)*ca)*(-sintheta*costheta*cosphi)+(-sb*cb*(1-ca))*(-sintheta*costheta*sinphi)+(-cb*sa)*(-sintheta*(-sintheta))))
	Eyy = exp(1im*phase)*L*(((-sb*cb*(1-ca))*(-sintheta*costheta*cosphi)+((cb)^2+(1-(cb)^2)*ca)*(-sintheta*costheta*sinphi)+(-sb*sa)*(-sintheta*(-sintheta))))
	Ezz = exp(1im*phase)*L*(((cb*sa)*(-sintheta*costheta*cosphi)+(sb*sa)*(-sintheta*costheta*sinphi)+ca*(-sintheta*(-sintheta))))
	ETheta= Exx*cos(theta)*cos(phi)+Eyy*cos(theta)*sin(phi)-Ezz*sin(theta)
	EPhi= -Exx*sin(phi)+Eyy*cos(phi)
	#Er = Exx*sin(theta)*cos(phi)+Eyy*sin(theta)*sin(phi)+Ezz*cos(theta)
    return ETheta,EPhi
end

const  nf=30
const ka=logspace(-1,0.69999997,nf)	#linspace(0.1,20,200) #valeurs de $ka$ désirées
const R_eut=1. 			#Rayon de l'objet sphérique en m
const freq=ka*c/2/pi/R_eut

const R = 1000 #distance en m du point de mesure

const N=50
const M=10000
const n_dipole=20

resth=zeros(nf,n_dipole)
resph=zeros(nf,n_dipole)

using HDF5, JLD

for n=1:n_dipole
    phi=2*pi*rand(N);
    theta=acos(2*rand(N).-1);
    for j=1:M 
		tic()
        #création de l'objet rayonnant
        theta_eut=acos(2*rand(n,1).-1);
        phi_eut=2*pi*rand(n,1);
        x=R_eut.*cos(phi_eut).*sin(theta_eut);
        y=R_eut.*sin(phi_eut).*sin(theta_eut);
        z=R_eut.*cos(theta_eut);
        tilt=acos(2*rand(n,1).-1);
        azimut=2*pi*rand(n,1);
        ld=.1;
        amplitude=ones(n)*ld;
        phas=2*pi*rand(n);
        for f=1:nf;
			Eth=complex(zeros(N));
			Eph=complex(zeros(N));
			for p=1:N;
				for i=1:n
					Et,Ep=Efarfield(R,theta[p],phi[p],[x[i],y[i],z[i],tilt[i],azimut[i],amplitude[i],phas[i]],freq[f]);
					Eth[p]=Et+Eth[p];
					Eph[p]=Ep+Eph[p];
				end
			end
			resth[f,n]+=ADTest(abs(Eth),"Rayleigh");
			resph[f,n]+=ADTest(abs(Eph),"Rayleigh");
		end
		if mod(j,1000)==0
			println("$n dip., $j/$M")
			toc()
			tic()
		end	
	end
	@save "resth.jld" resth ka freq
	@save "resph.jld" resph ka freq
end



using PyPlot
figure(1)
pcolor(linspace(1,20,20),ka,1.-resth./M)
xlabel("\$ n\$")
ylabel("\$ka\$")
xlim(1,20)
ylim(0.1,5)
colorbar()
clim(0,1)
savefig("eth.png")


figure(2)
pcolor(linspace(1,20,20),ka,1.-resph./M)
xlabel("\$ n\$")
ylabel("\$ka\$")
xlim(1,20)
ylim(0.1,5)
colorbar()
clim(0,1)
savefig("eph.png")