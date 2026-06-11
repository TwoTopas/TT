# 第2批抓取指令

在Chrome Console里执行以下命令，把结果贴给我。

## 命令1：搜细分行业/垂直市场
```javascript
let subs = ['sweatystartup','smallbusiness','Entrepreneur','sidehustle','microsaas','saas','startups'];
Promise.all(subs.map(s=>fetch('https://www.reddit.com/r/'+s+'/search.json?q=niche+software+OR+service+business+OR+field+service+OR+dispatching&sort=top&t=year&limit=3').then(r=>r.json()))).then(d=>d.forEach((data,i)=>{if(data.data)console.log('=== '+subs[i]+' ===',JSON.stringify(data.data.children.map(x=>'⭐'+x.data.score+' '+x.data.title),null,2))}))
```

## 命令2：搜"what software do you use"这类真实需求
```javascript
let qs = ['"what software" "service business" site:reddit.com','"looking for" "software" "manage" site:reddit.com','"anyone using" software for site:reddit.com'];
// 用 search 参数
let subs2 = ['smallbusiness','sweatystartup','Entrepreneur'];
Promise.all(subs2.map(s=>fetch('https://www.reddit.com/r/'+s+'/search.json?q=what+software+do+you+use&sort=top&t=year&limit=5').then(r=>r.json()))).then(d=>d.forEach((data,i)=>{if(data.data)console.log('=== '+subs2[i]+' ===',JSON.stringify(data.data.children.map(x=>'⭐'+x.data.score+' '+x.data.title),null,2))}))
```

## 命令3：搜最无聊/最被忽视的生意的真实讨论
```javascript
let subs3 = ['sweatystartup','Entrepreneur'];
Promise.all(subs3.map(s=>fetch('https://www.reddit.com/r/'+s+'/search.json?q=boring+business+niche&sort=top&t=year&limit=5').then(r=>r.json()))).then(d=>d.forEach((data,i)=>{if(data.data)console.log('=== '+subs3[i]+' ===',JSON.stringify(data.data.children.map(x=>'⭐'+x.data.score+' '+x.data.title),null,2))}))
```
