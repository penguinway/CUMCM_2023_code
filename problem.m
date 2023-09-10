load matlab.mat
months = [1 2 3 4 5 6 7 8 9 10 11 12];
times = [9, 10.5, 12, 13.5, 15];
D = [-59, -28, 0, 31, 61, 92, 122, 153, 184, 214, 245, 275];
plus = [[-6,6]',[6,6]',[-6,-6]',[6,-6]'];
S = 0;
X = [];
Y = [];
sideS = [];
s_save = [];
result = [];
data = data * 0.8;
for i = 1:3332
    result = [result,0];
end
for i = 1:12
    for j = 1:5
        d = D(i);
        sin_rou = sin(2*pi*d/365)*sin(2*(pi/360)*23.45);
        omiga = pi/12*(times(j) - 12);
        sin_as = cos(asin(sin_rou))*cos((39.4/180)*pi)*cos(omiga)+sin_rou*sin((39.4/180)*pi);
        cos_ys = (sin_rou - sin_as*sin((39.4/180)*pi))/cos(asin(sin_rou))*cos((39.4/180)*pi);
        I = [-cos(asin(sin_as))*sin(acos(cos_ys)), -cos(asin(sin_as))*cos_ys, -sin(acos(cos_ys))];
        for k = 1:3332    
            TA = outmat(data(k,1:3),I);
            for l = 1:3332
                if (sqrt((data(k,1)-data(l,1))^2 +(data(k,2)-data(l,2))^2+(data(k,3)-data(l,3))^2) < 50 && l ~= k)
                    TB = outmat(data(l,1:3),I);
                    sideS_ = outS(TA,TB,data(k,1:3),data(l,1:3),I,3,3);
                    result(l) = result(l) + sideS_;
                end
            end
        end
        eval("result"+int2str(i)+"_"+int2str(j)+"=[];")
        eval("result"+int2str(i)+"_"+int2str(j)+"=result';")
        % eval("xlswrite('result_"+int2str(i)+"_"+int2str(j)+".xlsx',"+"result"+int2str(i)+"_"+int2str(j)+");")
        result = [];
        for a1111 = 1:3332
            result = [result,0];
        end
    end
end
function T = outmat(R,I)
    R = [-R(1), -R(2), 84-R(3)];
    n = (R - I)/norm(R - I);
    cos_fi = n(3);
    fi = acos(cos_fi);
    theta = acos(n(2)/(-sin(fi)));
    aipu = [cos(fi), sin(fi), 0];
    y = [-cos(fi)*sin(theta), cos(fi)*cos(theta), sin(fi)];
    T = [aipu', y', n'];
end
function r = cal(Ta,Tb,La,A,B,I)
    H1_ = Tb*La +A;
    H2__ = Tb'*(H1_-B);
    abc = Tb*I';
    x_tou = H2__(1)-(abc(1)/abc(3))*H2__(3);
    y_tou = H2__(2)-(abc(2)/abc(3))*H2__(3);
    r = [x_tou,y_tou];
end
function sideS = outS(Ta,Tb,Ra,Rb,I,a,b)
    r1 = cal(Ta,Tb,[a/2,b/2,0]',Ra,Rb,I);
    r2 = cal(Ta,Tb,[-a/2,b/2,0]',Ra,Rb,I);
    r3 = cal(Ta,Tb,[-a/2,-b/2,0]',Ra,Rb,I);
    r4 = cal(Ta,Tb,[a/2,-b/2,0]',Ra,Rb,I);
    r_ = [r1',r2',r3',r4'];
    for i=1:4
        if r_(1,i)>-a/2 && r_(1,i)<a/2 && r_(2,i)>-b/2 && r_(2,i)<b/2
            zero__ = cal(Ta,Tb,[0,0,0]',Ra,Rb,I);
            if zero__(1)>0 && zero__(2)>0
                m=1;
            elseif zero__(1)<0 && zero__(2)>0
                m=2;
            elseif zero__(1)<0 && zero__(2)<0
                m=3;
            else
                m=4;
            end
        else
            m=0;
        end
        if m == 0
            sideS = 0;
        elseif m == 1
            sideS = (a/2 - r_(1,i))*(b/2 - r_(1,i));
        elseif m == 2
            sideS = (a/2 + r_(1,i))*(b/2 - r_(1,i));
        elseif m == 3
            sideS = (a/2 + r_(1,i))*(b/2 + r_(2,i));
        else
            sideS = (a/2 - r_(1,i))*(b/2 + r_(2,i));
        end
    end
end

