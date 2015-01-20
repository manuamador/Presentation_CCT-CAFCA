function ADTest(X,distribution,alpha=0.05)
"""
Anderson Darling statistical test for Rayleigh or exponential distribution
return 0 if the distribution follows the given distribution, 1 otherwise.

X: vector, N samples (30<N<150)
distribution: string 'Rayleigh' or 'Exponential'
alpha: typical statistical error
"""

	N=length(X)
	
	#Stephen's critical values
	if alpha==0.15
		CV=0.922
	elseif alpha==0.10
		CV=1.078
	elseif alpha==0.05
		CV=1.341
	elseif alpha==0.025
		CV=1.606
	elseif alpha==0.01
		CV=1.957
	end
	if distribution=="Rayleigh"
		b=mean(X)/sqrt(pi/2); #get the shape parameter
		x= minimum(X):(maximum(X)-minimum(X))/(N-1):maximum(X); 
		y=sort(X);
		CDF = 1.-exp(-y.^2/2b^2); # theoretical CDF
		Stat=log(CDF)+log(1.-flipud(CDF));
	elseif distribution=="Exponential"
		b=1/mean(X); #get the scale parameter
		x= minimum(X):(maximum(X)-minimum(X))/(N-1):maximum(X); 
		y=sort(X);
		CDF = 1.-exp(-b.*y); # theoretical CDF
		Stat=log(CDF)+log(1.-flipud(CDF));
	end
	
	A=[];
    for i=1:N
        A=[A;(2*i-1)*Stat[i]];
    end
    Astat=-sum(A)/N-N;
    if Astat*(1+0.6/N)>CV #test
        result=1;
    else
        result=0;
    end
	return result
end