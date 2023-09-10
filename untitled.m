load answer.mat
result = [];
for i = 1:12
    for j = 1:5
        eval("result=[result,result"+int2str(i)+"_"+int2str(j)+"];")
    end
end