-- Banc déterministe sans bibliothèque Roblox, réseau ni horloge système.
local banc = {}
local natif = getfenv()
local maintenant, epoch, ordre = 0, 1704067200, 0
local file, annules, avertissements = {}, {}, {}
local task = {}
local function manque(api) error("API non simulée : " .. api, 2) end
local function strict(t, nom)
    return setmetatable(t, {__index=function(_, k) manque(nom .. "." .. tostring(k)) end})
end
local function planifier(co, date, args)
    ordre += 1
    table.insert(file, {co=co, date=date, args=args or table.pack(), ordre=ordre})
    return co
end
function task.spawn(f, ...) return planifier(if type(f)=="thread" then f else coroutine.create(f), maintenant, table.pack(...)) end
function task.defer(f, ...) return task.spawn(f, ...) end
function task.delay(d, f, ...)
    assert(d>=0, "délai négatif")
    return planifier(if type(f)=="thread" then f else coroutine.create(f), maintenant+d, table.pack(...))
end
function task.cancel(co) annules[co]=true end
function task.wait(d) return coroutine.yield({delai=math.max(d or 0, 1/60)}) end
local function signal()
    local s={_type="RBXScriptSignal",connexions={}}
    function s:Connect(f)
        local c={_type="RBXScriptConnection",Connected=true, f=f}
        function c:Disconnect() self.Connected=false end
        table.insert(self.connexions,c); return c
    end
    function s:Once(f)
        local c; c=self:Connect(function(...) c:Disconnect(); f(...) end); return c
    end
    function s:Wait()
        local co=coroutine.running()
        self:Once(function(...) planifier(co,maintenant,table.pack(...)) end)
        return coroutine.yield()
    end
    function s:Fire(...)
        for _,c in ipairs(table.clone(self.connexions)) do if c.Connected then task.spawn(c.f,...) end end
    end
    return strict(s,"RBXScriptSignal")
end
local heartbeat, stepped, prochainPas=signal(), signal(), 1/60
function banc.avancer(secondes)
    assert(type(secondes)=="number" and secondes>=0 and secondes<math.huge,"durée invalide")
    local cible, iterations=maintenant+secondes, 0
    while true do
        local idx, suivant
        for i,t in ipairs(file) do
            if not suivant or t.date<suivant.date or (t.date==suivant.date and t.ordre<suivant.ordre) then idx,suivant=i,t end
        end
        local cadence=false
        for _,s in ipairs({heartbeat,stepped}) do for _,c in ipairs(s.connexions) do if c.Connected then cadence=true end end end
        if cadence and prochainPas<=cible and (not suivant or prochainPas<suivant.date) then
            maintenant=prochainPas; prochainPas+=1/60
            stepped:Fire(maintenant,1/60); heartbeat:Fire(1/60)
        elseif suivant and suivant.date<=cible then
            table.remove(file,idx); maintenant=math.max(maintenant,suivant.date)
            if not annules[suivant.co] then
                local ok,r=coroutine.resume(suivant.co,table.unpack(suivant.args,1,suivant.args.n))
                if not ok then error(debug.traceback(suivant.co,tostring(r)),0) end
                if coroutine.status(suivant.co)~="dead" and type(r)=="table" and r.delai then
                    planifier(suivant.co,maintenant+r.delai,table.pack(r.delai))
                end
            end
        else break end
        iterations+=1; assert(iterations<5000000,"ordonnanceur : trop d'étapes")
    end
    maintenant=cible
    if prochainPas<=maintenant then prochainPas=maintenant+1/60 end
end
local function genre(v) return if type(v)=="table" and rawget(v,"_type") then rawget(v,"_type") else typeof(v) end
local function vecteur(nom,dimensions)
    local constructeur,mt={},{}
    function constructeur.new(...)
        local a={...}; local v={_type=nom}
        for i,k in ipairs(dimensions) do v[k]=a[i] or 0 end
        return setmetatable(v,mt)
    end
    local function op(a,b,f)
        local r={}; for i,k in ipairs(dimensions) do r[i]=f(if type(a)=="number" then a else a[k],if type(b)=="number" then b else b[k]) end
        return constructeur.new(table.unpack(r))
    end
    mt.__add=function(a,b) return op(a,b,function(x,y) return x+y end) end
    mt.__sub=function(a,b) return op(a,b,function(x,y) return x-y end) end
    mt.__mul=function(a,b) return op(a,b,function(x,y) return x*y end) end
    mt.__div=function(a,b) return op(a,b,function(x,y) return x/y end) end
    mt.__unm=function(a) return a*-1 end
    mt.__eq=function(a,b) for _,k in ipairs(dimensions) do if a[k]~=b[k] then return false end end; return true end
    mt.__index=function(v,k)
        if k=="Magnitude" then local s=0; for _,d in ipairs(dimensions) do s+=v[d]^2 end; return math.sqrt(s) end
        if k=="Unit" then return v/v.Magnitude end
        if k=="Dot" then return function(a,b) local s=0; for _,d in ipairs(dimensions) do s+=a[d]*b[d] end; return s end end
        if k=="Cross" and #dimensions==3 then return function(a,b) return constructeur.new(a.Y*b.Z-a.Z*b.Y,a.Z*b.X-a.X*b.Z,a.X*b.Y-a.Y*b.X) end end
        if k=="Lerp" then return function(a,b,t) return a+(b-a)*t end end
        manque(nom.."."..k)
    end
    constructeur.zero=constructeur.new(); constructeur.one=constructeur.new(1,1,1)
    return strict(constructeur,nom)
end
local Vector3,Vector2=vecteur("Vector3",{"X","Y","Z"}),vecteur("Vector2",{"X","Y"})
-- CFrame : rotation matricielle et translation, sans moteur physique.
local CFrame,cfmt={},{}
function CFrame.new(x,y,z,...)
    assert(y==nil or type(y)=="number","API non simulée : CFrame.new(position, cible) ; utiliser CFrame.lookAt")
    local a={...}; local p=if genre(x)=="Vector3" then x else Vector3.new(x,y,z)
    return setmetatable({_type="CFrame",Position=p,r=if #a==9 then a else {1,0,0,0,1,0,0,0,1}},cfmt)
end
local function rotation(c,v)
    local r=c.r; return Vector3.new(r[1]*v.X+r[2]*v.Y+r[3]*v.Z,r[4]*v.X+r[5]*v.Y+r[6]*v.Z,r[7]*v.X+r[8]*v.Y+r[9]*v.Z)
end
cfmt.__mul=function(a,b)
    if genre(b)=="Vector3" then return a.Position+rotation(a,b) end
    local r={}; for i=0,2 do for j=1,3 do r[i*3+j]=0; for k=1,3 do r[i*3+j]+=a.r[i*3+k]*b.r[(k-1)*3+j] end end end
    local p=a.Position+rotation(a,b.Position); return CFrame.new(p.X,p.Y,p.Z,table.unpack(r))
end
cfmt.__add=function(a,b) local p=a.Position+b; return CFrame.new(p.X,p.Y,p.Z,table.unpack(a.r)) end
cfmt.__sub=function(a,b) return a+(-b) end
cfmt.__index=function(c,k)
    if k=="X" or k=="Y" or k=="Z" then return c.Position[k] end
    if k=="Inverse" then return function(a)
        local r=a.r; local b=CFrame.new(0,0,0,r[1],r[4],r[7],r[2],r[5],r[8],r[3],r[6],r[9]); return b+rotation(b,-a.Position)
    end end
    if k=="ToWorldSpace" or k=="PointToWorldSpace" then return function(a,b) return a*b end end
    if k=="ToObjectSpace" or k=="PointToObjectSpace" then return function(a,b) return a:Inverse()*b end end
    if k=="VectorToWorldSpace" then return function(a,b) return rotation(a,b) end end
    if k=="VectorToObjectSpace" then return function(a,b) return rotation(a:Inverse(),b) end end
    if k=="GetComponents" then return function(a) return a.X,a.Y,a.Z,table.unpack(a.r) end end
    if k=="LookVector" then return Vector3.new(-c.r[3],-c.r[6],-c.r[9]) end
    if k=="RightVector" then return Vector3.new(c.r[1],c.r[4],c.r[7]) end
    if k=="UpVector" then return Vector3.new(c.r[2],c.r[5],c.r[8]) end
    manque("CFrame."..k)
end
function CFrame.Angles(x,y,z)
    local cx,sx,cy,sy,cz,sz=math.cos(x),math.sin(x),math.cos(y),math.sin(y),math.cos(z),math.sin(z)
    return CFrame.new(0,0,0,cy*cz,-cy*sz,sy,cx*sz+sx*sy*cz,cx*cz-sx*sy*sz,-sx*cy,sx*sz-cx*sy*cz,sx*cz+cx*sy*sz,cx*cy)
end
CFrame.fromEulerAnglesXYZ=CFrame.Angles; CFrame.identity=CFrame.new()
CFrame.fromOrientation=CFrame.Angles
function CFrame.lookAt(position,cible,haut)
    local z=(position-cible).Unit
    local x=(haut or Vector3.new(0,1,0)):Cross(z).Unit
    local y=z:Cross(x)
    return CFrame.new(position.X,position.Y,position.Z,x.X,y.X,z.X,x.Y,y.Y,z.Y,x.Z,y.Z,z.Z)
end
local function donnees(nom,champs)
    return strict({new=function(...)
        local a={...}; local r={_type=nom}; for i,k in ipairs(champs) do r[k]=a[i] or 0 end
        return strict(r,nom)
    end},nom)
end
local Color3=donnees("Color3",{"R","G","B"})
function Color3.fromRGB(r,g,b) return Color3.new(r/255,g/255,b/255) end
function Color3.fromHSV(h,s,v)
    local function canal(n) local k=(n+h*6)%6; return v-v*s*math.max(0,math.min(k,4-k,1)) end
    return Color3.new(canal(5),canal(3),canal(1))
end
local UDim=donnees("UDim",{"Scale","Offset"})
local UDim2={new=function(a,b,c,d) return strict({_type="UDim2",X=UDim.new(a,b),Y=UDim.new(c,d)},"UDim2") end}
function UDim2.fromScale(x,y) return UDim2.new(x,0,y,0) end
function UDim2.fromOffset(x,y) return UDim2.new(0,x,0,y) end
local NumberRange={new=function(a,b) return strict({_type="NumberRange",Min=a,Max=b or a},"NumberRange") end}
local TweenInfo={new=function(t,style,direction,repeats,reverses,delai)
    return {_type="TweenInfo",Time=t or 1,EasingStyle=style,EasingDirection=direction,RepeatCount=repeats or 0,Reverses=reverses or false,DelayTime=delai or 0}
end}
local Random={}
function Random.new(seed)
    local etat=math.max(1,(seed or 1)%2147483647); local r={_type="Random"}
    function r:NextNumber(a,b) etat=(etat*48271)%2147483647; return (a or 0)+(etat/2147483647)*((b or 1)-(a or 0)) end
    function r:NextInteger(a,b) return math.floor(self:NextNumber(a,b+1)) end
    function r:Clone() return Random.new(etat) end
    return strict(r,"Random")
end
local function enum(chemin)
    return setmetatable({_type="EnumItem",Name=chemin:match("[^.]+$")},{__index=function(t,k) local v=enum(chemin.."."..k); rawset(t,k,v); return v end,__tostring=function() return chemin end})
end
local Enum=enum("Enum")
local Instance,methodes,imt={},{},{}
local classes={Folder=true,RemoteEvent=true,RemoteFunction=true,BindableEvent=true,BindableFunction=true,Part=true,Model=true,Sound=true,ScreenGui=true,Player=true,ModuleScript=true,Script=true,LocalScript=true}
local interfaces={Frame=true,TextLabel=true,TextButton=true,TextBox=true,ImageLabel=true,ImageButton=true,ScrollingFrame=true,UIListLayout=true,UIGridLayout=true,UICorner=true,UIStroke=true,UIPadding=true,UIScale=true,UIAspectRatioConstraint=true,UISizeConstraint=true,BillboardGui=true,SurfaceGui=true}
local valeurs={BoolValue=false,IntValue=0,NumberValue=0,StringValue="",Vector3Value=Vector3.zero,CFrameValue=CFrame.identity,Color3Value=Color3.new(),ObjectValue=false}
function Instance.new(classe,parent)
    assert(classes[classe] or interfaces[classe] or valeurs[classe]~=nil,"API non simulée : Instance.new("..tostring(classe)..")")
    local p={Name=classe,ClassName=classe,Archivable=true}
    if valeurs[classe]~=nil and classe~="ObjectValue" then p.Value=valeurs[classe] end
    if classe=="Player" then p.UserId=0; p.LocaleId="fr-fr"; p.DisplayName="Joueur" end
    if classe=="Part" then p.Position=Vector3.zero; p.CFrame=CFrame.identity; p.Size=Vector3.one; p.Anchored=false; p.CanCollide=true; p.Transparency=0 end
    if classe=="Sound" then p.IsPlaying=false; p.Volume=1; p.Looped=false; p.SoundId="" end
    local s={Changed=signal(),ChildAdded=signal(),ChildRemoved=signal(),Destroying=signal()}
    if classe=="RemoteEvent" then s.OnServerEvent=signal(); s.OnClientEvent=signal() end
    if classe=="BindableEvent" then s.Event=signal() end
    local v=setmetatable({_type="Instance",_p=p,_s=s,_enfants={},_attributs={},_as={},_ps={},_messages={}},imt)
    if parent then v.Parent=parent end; return v
end
imt.__index=function(v,k)
    if methodes[k] then return methodes[k] end
    if v._p[k]~=nil then return v._p[k] end
    if v._s[k] then return v._s[k] end
    for _,c in ipairs(v._enfants) do if c.Name==k then return c end end
    if k=="Parent" or k=="OnServerInvoke" or k=="OnInvoke" or k=="Character" or k=="PrimaryPart" or (k=="Value" and v.ClassName=="ObjectValue") then return nil end
    manque(v.ClassName.."."..k)
end
imt.__newindex=function(v,k,x)
    local ancien=v._p[k]; if ancien==x then return end
    if k=="Parent" then
        if x then local a=x; while a do assert(a~=v,"Parent cyclique"); a=a.Parent end end
        if ancien then local i=table.find(ancien._enfants,v); if i then table.remove(ancien._enfants,i) end; ancien.ChildRemoved:Fire(v) end
        v._p[k]=x
        if x then table.insert(x._enfants,v); x.ChildAdded:Fire(v) end
    else v._p[k]=x end
    v.Changed:Fire(if valeurs[v.ClassName]~=nil then x else k)
    if v._ps[k] then v._ps[k]:Fire() end
end
function methodes:GetChildren() return table.clone(self._enfants) end
function methodes:GetDescendants() local r={}; for _,c in ipairs(self._enfants) do table.insert(r,c); for _,d in ipairs(c:GetDescendants()) do table.insert(r,d) end end; return r end
function methodes:FindFirstChild(n,rec) for _,v in ipairs(if rec then self:GetDescendants() else self._enfants) do if v.Name==n then return v end end; return nil end
function methodes:FindFirstChildOfClass(c) for _,v in ipairs(self._enfants) do if v.ClassName==c then return v end end; return nil end
function methodes:WaitForChild(n) local v=self:FindFirstChild(n); assert(v,"WaitForChild absent : "..self:GetFullName().."."..n); return v end
function methodes:IsA(c) return c=="Instance" or self.ClassName==c or (c=="ValueBase" and valeurs[self.ClassName]~=nil) or (c=="BasePart" and self.ClassName=="Part") or (c=="GuiObject" and interfaces[self.ClassName]==true) end
function methodes:GetFullName() return if self.Parent then self.Parent:GetFullName().."."..self.Name else self.Name end
function methodes:GetPropertyChangedSignal(k) if not self._ps[k] then self._ps[k]=signal() end; return self._ps[k] end
function methodes:SetAttribute(k,v) if self._attributs[k]==v then return end; self._attributs[k]=v; if self._as[k] then self._as[k]:Fire() end end
function methodes:GetAttribute(k) return self._attributs[k] end
function methodes:GetAttributes() return table.clone(self._attributs) end
function methodes:GetAttributeChangedSignal(k) if not self._as[k] then self._as[k]=signal() end; return self._as[k] end
function methodes:Destroy() self.Destroying:Fire(); for _,c in ipairs(self:GetChildren()) do c:Destroy() end; self.Parent=nil; for _,s in pairs(self._s) do for _,c in ipairs(s.connexions) do c:Disconnect() end end end
function methodes:Clone()
    local correspondances={}
    local function copier(v)
        local c=Instance.new(v.ClassName); correspondances[v]=c
        for k,x in pairs(v._p) do if k~="Parent" then c._p[k]=x end end
        c._attributs=table.clone(v._attributs)
        for _,e in ipairs(v._enfants) do if e.Archivable then copier(e).Parent=c end end; return c
    end
    local r=copier(self)
    for _,c in pairs(correspondances) do for k,x in pairs(c._p) do if correspondances[x] then c._p[k]=correspondances[x] end end end
    return r
end
function methodes:Fire(...) assert(self.ClassName=="BindableEvent"); self.Event:Fire(...) end
function methodes:Invoke(...) assert(self.ClassName=="BindableFunction"); return self.OnInvoke(...) end
function methodes:FireClient(j,...) assert(self.ClassName=="RemoteEvent"); if not self._messages[j] then self._messages[j]={} end; table.insert(self._messages[j],table.pack(...)) end
function methodes:FireAllClients(...) for _,j in ipairs(banc._joueurs) do self:FireClient(j,...) end end
function methodes:Kick(raison) self:SetAttribute("Kick",raison or ""); banc.quitter(self) end
function methodes:Play() assert(self.ClassName=="Sound"); self.IsPlaying=true end
function methodes:Stop() assert(self.ClassName=="Sound"); self.IsPlaying=false end
-- JSON strict : cycles, clés mixtes, NaN, instances et fonctions refusés.
local function encoder(v,pile)
    local t=type(v)
    if t=="nil" then return "null" end
    if t=="boolean" then return tostring(v) end
    if t=="number" then assert(v==v and math.abs(v)<math.huge,"JSON : nombre non fini"); return string.format("%.17g",v) end
    if t=="string" then assert(utf8.len(v),"JSON : UTF-8 invalide"); return '"'..v:gsub('[%z\1-\31\\"]',function(c)
        local ech={['"']='\\"',['\\']='\\\\',['\n']='\\n',['\r']='\\r',['\t']='\\t'}
        return ech[c] or string.format("\\u%04x",string.byte(c))
    end)..'"' end
    assert(t=="table" and getmetatable(v)==nil,"JSON : valeur non sérialisable")
    pile=pile or {}; assert(not pile[v],"JSON : cycle"); pile[v]=true
    local n,chaine,nombre=0,false,false
    for k in pairs(v) do n+=1; if type(k)=="string" then chaine=true else assert(type(k)=="number" and k>=1 and k%1==0,"JSON : clé invalide"); nombre=true end end
    assert(not (chaine and nombre),"JSON : clés mixtes")
    local r={}
    if nombre then assert(#v==n,"JSON : tableau creux"); for i=1,n do table.insert(r,encoder(v[i],pile)) end
    else local cles={}; for k in pairs(v) do table.insert(cles,k) end; table.sort(cles); for _,k in ipairs(cles) do table.insert(r,encoder(k)..":"..encoder(v[k],pile)) end end
    pile[v]=nil; return (if nombre then "[" else "{")..table.concat(r,",")..(if nombre then "]" else "}")
end
local function decoder(s)
    local i=1; local lire
    local function blanc() local _,fin=s:find("^%s*",i); i=(fin or i-1)+1 end
    local function texte()
        assert(s:sub(i,i)=='"',"JSON : chaîne attendue"); i+=1; local r={}
        while i<=#s do
            local c=s:sub(i,i); i+=1
            if c=='"' then return table.concat(r) end
            if c=='\\' then
                c=s:sub(i,i); i+=1
                local e={['"']='"',['\\']='\\',['/']='/',b='\b',f='\f',n='\n',r='\r',t='\t'}
                if c=='u' then
                    local h=s:sub(i,i+3); assert(h:match('^%x%x%x%x$'),"JSON : unicode invalide"); local code=tonumber(h,16); i+=4
                    if code>=0xD800 and code<=0xDBFF then
                        assert(s:sub(i,i+1)=='\\u',"JSON : surrogate absent"); local bas=tonumber(s:sub(i+2,i+5),16)
                        assert(bas and bas>=0xDC00 and bas<=0xDFFF,"JSON : surrogate invalide"); i+=6; code=0x10000+(code-0xD800)*1024+bas-0xDC00
                    end
                    assert(code<0xD800 or code>0xDFFF,"JSON : surrogate isolé"); table.insert(r,utf8.char(code))
                else assert(e[c],"JSON : échappement invalide"); table.insert(r,e[c]) end
            else assert(string.byte(c)>=32,"JSON : caractère de contrôle"); table.insert(r,c) end
        end
        error("JSON : chaîne inachevée")
    end
    lire=function()
        blanc(); local c=s:sub(i,i)
        if c=='"' then return texte() end
        if c=='{' or c=='[' then
            local objet=c=='{'; local fin=if objet then '}' else ']'; local r={}; i+=1; blanc()
            if s:sub(i,i)==fin then i+=1; return r end
            local indice=0
            while true do
                indice+=1; local k=if objet then texte() else indice
                if objet then blanc(); assert(s:sub(i,i)==':',"JSON : deux-points attendu"); i+=1 end
                r[k]=lire(); blanc(); c=s:sub(i,i); i+=1
                if c==fin then return r end
                assert(c==',',"JSON : virgule attendue"); blanc()
            end
        end
        for mot,v in pairs({['true']=true,['false']=false}) do if s:sub(i,i+#mot-1)==mot then i+=#mot; return v end end
        if s:sub(i,i+3)=='null' then i+=4; return nil end
        local debut=i
        if s:sub(i,i)=='-' then i+=1 end
        if s:sub(i,i)=='0' then i+=1 else assert(s:sub(i,i):match('[1-9]'),"JSON : nombre attendu"); repeat i+=1 until not s:sub(i,i):match('%d') end
        if s:sub(i,i)=='.' then i+=1; assert(s:sub(i,i):match('%d'),"JSON : décimale absente"); repeat i+=1 until not s:sub(i,i):match('%d') end
        if s:sub(i,i):lower()=='e' then i+=1; if s:sub(i,i):match('[+-]') then i+=1 end; assert(s:sub(i,i):match('%d'),"JSON : exposant absent"); repeat i+=1 until not s:sub(i,i):match('%d') end
        local n=tonumber(s:sub(debut,i-1)); assert(n and math.abs(n)<math.huge,"JSON : nombre invalide"); return n
    end
    local r=lire(); blanc(); assert(i>#s,"JSON : suffixe inattendu"); return r
end
local function copie(v) return decoder(encoder(v)) end
local services,fermeture={},{}
local game={PlaceId=0,PlaceVersion=1,JobId="banc-0001"}
function game:GetService(n) assert(services[n],"API non simulée : game:GetService("..n..")"); return services[n] end
function game:BindToClose(f) table.insert(fermeture,f) end
setmetatable(game,{__index=function(_,k) if services[k] then return services[k] end; manque("game."..k) end})
for _,n in ipairs({"ReplicatedStorage","ReplicatedFirst","ServerScriptService","ServerStorage","StarterPlayer","StarterGui","StarterPack","Workspace","Lighting","SoundService"}) do local s=Instance.new("Folder"); s.Name=n; services[n]=s end
local function service(n,t) services[n]=strict(t,n); return services[n] end
banc._joueurs={}
local Players=service("Players",{PlayerAdded=signal(),PlayerRemoving=signal()})
function Players:GetPlayers() return table.clone(banc._joueurs) end
function Players:GetPlayerByUserId(id) for _,p in ipairs(banc._joueurs) do if p.UserId==id then return p end end; return nil end
function banc.joueur(id,nom,options)
    assert(not Players:GetPlayerByUserId(id),"joueur déjà présent")
    local j=Instance.new("Player"); j.UserId=id; j.Name=nom or "Joueur"..id; j.DisplayName=j.Name
    for k,v in pairs(options or {}) do j[k]=v end
    table.insert(banc._joueurs,j); Players.PlayerAdded:Fire(j); banc.avancer(0); return j
end
function banc.quitter(j) local i=table.find(banc._joueurs,j); assert(i,"joueur absent"); Players.PlayerRemoving:Fire(j); banc.avancer(0); table.remove(banc._joueurs,i) end
local mode={studio=true,serveur=true,client=false}
service("RunService",{Heartbeat=heartbeat,Stepped=stepped,IsStudio=function() return mode.studio end,IsServer=function() return mode.serveur end,IsClient=function() return mode.client end})
function banc.studio(v) mode.studio=v end
function banc.mode(serveur,client) mode.serveur=serveur; mode.client=client end
local guid=0
service("HttpService",{JSONEncode=function(_,v) return encoder(v) end,JSONDecode=function(_,v) return decoder(v) end,GenerateGUID=function(_,accolades) guid+=1; local s=string.format("00000000-0000-4000-8000-%012d",guid); return if accolades==false then s else "{"..s.."}" end})
local magasins={}
-- Profil de stress demande : anciennes bornes conservatrices, pas les limites Roblox actuelles.
-- Les tests unitaires restent instantanes ; les parcours activent explicitement ce profil.
local datastoreLatence, datastoreLimites = 0, false
local ecrituresServeur = {}
function banc.configurer_datastore(options)
    assert(type(options.latence_s)=="number" and options.latence_s>=0 and options.latence_s<math.huge,"latence invalide")
    assert(type(options.limites)=="boolean","limites booleennes attendues")
    datastoreLatence=options.latence_s; datastoreLimites=options.limites
end
local function magasin(n,scope,ordonne)
    local cle=n.."\0"..(scope or "global")..(if ordonne then "\0ordered" else "")
    if magasins[cle] then return magasins[cle].api end
    local etat={valeurs={},userIds={},appels=0,par_methode={},prochains=0,permanente=false,dernieres={},ecritures={},refus_cle=0,refus_budget=0}; local api={}
    local function appel(m,k)
        etat.appels+=1; etat.par_methode[m]=(etat.par_methode[m] or 0)+1
        if datastoreLatence>0 then task.wait(datastoreLatence) end
        if etat.permanente or etat.prochains>0 then etat.prochains=math.max(0,etat.prochains-1); error("DataStore : panne injectée ("..m..")") end
        if k then assert(type(k)=="string","DataStore : clé chaîne attendue") end
    end
    local function budget(k)
        while #ecrituresServeur>0 and ecrituresServeur[1]<=maintenant-60 do table.remove(ecrituresServeur,1) end
        if datastoreLimites then
            if etat.dernieres[k] and maintenant-etat.dernieres[k]<6 then
                etat.refus_cle+=1; error("KeyThrottled : moins de 6 s entre ecritures (profil de stress)")
            end
            if #ecrituresServeur>=60+10*#Players:GetPlayers() then
                etat.refus_budget+=1; error("DatastoreThrottled : budget serveur par minute epuise (profil de stress)")
            end
        end
    end
    local function noter(k)
        table.insert(ecrituresServeur,maintenant); etat.dernieres[k]=maintenant
        table.insert(etat.ecritures,{cle=k,temps=maintenant})
    end
    local function sauver(k,v,ids)
        local json=encoder(v); assert(#json<=4*1024*1024,"DataStore : valeur supérieure à 4 Mo")
        local utilisateurs=if ids then copie(ids) else nil
        if ordonne then assert(type(v)=="number" and v%1==0,"OrderedDataStore : entier attendu") end
        budget(k)
        etat.valeurs[k]=decoder(json); if ids then etat.userIds[k]=utilisateurs end
        noter(k)
    end
    function api:GetAsync(k) appel("GetAsync",k); return copie(etat.valeurs[k]) end
    function api:SetAsync(k,v,ids) appel("SetAsync",k); sauver(k,v,ids) end
    function api:UpdateAsync(k,f) appel("UpdateAsync",k); local v,ids=f(copie(etat.valeurs[k])); if v~=nil then sauver(k,v,ids) end; return copie(etat.valeurs[k]) end
    function api:RemoveAsync(k) appel("RemoveAsync",k); budget(k); local v=etat.valeurs[k]; etat.valeurs[k]=nil; etat.userIds[k]=nil; noter(k); return copie(v) end
    function api:IncrementAsync(k,d,ids) appel("IncrementAsync",k); local v=(etat.valeurs[k] or 0)+(d or 1); sauver(k,v,ids); return v end
    function api:GetSortedAsync(asc,taille,mini,maxi)
        assert(ordonne,"GetSortedAsync exige OrderedDataStore"); appel("GetSortedAsync"); taille=taille or 50; assert(taille>0 and taille%1==0,"taille invalide")
        local lignes={}; for k,v in pairs(etat.valeurs) do if (not mini or v>=mini) and (not maxi or v<=maxi) then table.insert(lignes,{key=k,value=v}) end end
        table.sort(lignes,function(a,b) if a.value==b.value then return a.key<b.key end; return if asc then a.value<b.value else a.value>b.value end)
        local pos=1; local pages={IsFinished=#lignes<=taille}
        function pages:GetCurrentPage() local r={}; for i=pos,math.min(pos+taille-1,#lignes) do table.insert(r,copie(lignes[i])) end; return r end
        function pages:AdvanceToNextPageAsync() pos+=taille; self.IsFinished=pos+taille-1>=#lignes end
        return strict(pages,"DataStorePages")
    end
    etat.api=strict(api,"DataStore"); magasins[cle]=etat; return etat.api
end
service("DataStoreService",{GetDataStore=function(_,n,s) return magasin(n,s,false) end,GetOrderedDataStore=function(_,n,s) return magasin(n,s,true) end})
function banc.datastore(n,scope,ordonne)
    magasin(n,scope,ordonne); local e=magasins[n.."\0"..(scope or "global")..(if ordonne then "\0ordered" else "")]
    return {lire=function(_,k) return copie(e.valeurs[k]) end,pannes=function(_,n) e.prochains=n end,panne_permanente=function(_,v) e.permanente=v end,compteurs=function() return {total=e.appels,methodes=table.clone(e.par_methode),ecritures=#e.ecritures,refus_cle=e.refus_cle,refus_budget=e.refus_budget} end,historique=function() return copie(e.ecritures) end,userIds=function(_,k) return copie(e.userIds[k]) end}
end
local achats,passes,recus={},{},{}
local Marketplace=service("MarketplaceService",{prompts=achats})
function Marketplace:UserOwnsGamePassAsync(id,pass) return passes[tostring(id)..":"..pass]==true end
function Marketplace:PromptGamePassPurchase(j,id) table.insert(achats,{type="pass",joueur=j,id=id}) end
function Marketplace:PromptProductPurchase(j,id) table.insert(achats,{type="produit",joueur=j,id=id}) end
function banc.passe(j,id,v) passes[tostring(j.UserId)..":"..id]=v end
function banc.recu(j,id,purchaseId)
    local r={PlayerId=j.UserId,ProductId=id,PurchaseId=purchaseId or "achat-"..(#recus+1),CurrencySpent=0,PlaceIdWherePurchased=game.PlaceId}
    table.insert(recus,r); return Marketplace.ProcessReceipt(copie(r))
end
local evenements={}; local Analytics=service("AnalyticsService",{})
for _,n in ipairs({"LogCustomEvent","LogEconomyEvent","LogFunnelStepEvent","LogOnboardingFunnelStepEvent"}) do Analytics[n]=function(_,...) table.insert(evenements,{api=n,arguments=table.pack(...),temps=maintenant}) end end
function banc.analytics() return evenements end
local etiquettes={}; local Collection=service("CollectionService",{})
function Collection:AddTag(v,t) if not etiquettes[t] then etiquettes[t]={} end; etiquettes[t][v]=true end
function Collection:RemoveTag(v,t) if etiquettes[t] then etiquettes[t][v]=nil end end
function Collection:HasTag(v,t) return etiquettes[t]~=nil and etiquettes[t][v]==true end
function Collection:GetTagged(t) local r={}; for v in pairs(etiquettes[t] or {}) do table.insert(r,v) end; table.sort(r,function(a,b) return a:GetFullName()<b:GetFullName() end); return r end
function Collection:GetTags(v) local r={}; for t,vs in pairs(etiquettes) do if vs[v] then table.insert(r,t) end end; table.sort(r); return r end
service("LocalizationService",{RobloxLocaleId="fr-fr",SystemLocaleId="fr-fr",GetCountryRegionForPlayerAsync=function() return "FR" end})
service("TextService",{FilterStringAsync=function(_,texte) return strict({GetNonChatStringForBroadcastAsync=function() return texte end,GetNonChatStringForUserAsync=function() return texte end,GetChatForUserAsync=function() return texte end},"TextFilterResult") end})
local publications,abonnements,badges={},{},{}
service("MessagingService",{publications=publications,PublishAsync=function(_,sujet,data)
    table.insert(publications,{sujet=sujet,data=copie(data)}); if abonnements[sujet] then abonnements[sujet]:Fire({Data=copie(data),Sent=epoch+maintenant}) end
end,SubscribeAsync=function(_,sujet,f) if not abonnements[sujet] then abonnements[sujet]=signal() end; return abonnements[sujet]:Connect(f) end})
service("BadgeService",{attributions=badges,AwardBadgeAsync=function(_,id,badge) badges[tostring(id)..":"..badge]=true; return true end,UserHasBadgeAsync=function(_,id,badge) return badges[tostring(id)..":"..badge]==true end})
service("TweenService",{Create=function(_,objet,info,buts)
    assert(info.RepeatCount>=0,"API non simulée : Tween infini")
    local depart={}; for k in pairs(buts) do depart[k]=objet[k] end
    local co; local t={Completed=signal(),PlaybackState=Enum.PlaybackState.Begin}
    function t:Play()
        self.PlaybackState=Enum.PlaybackState.Playing
        co=task.delay(info.DelayTime+info.Time*(info.RepeatCount+1)*(if info.Reverses then 2 else 1),function()
            for k,v in pairs(if info.Reverses then depart else buts) do objet[k]=v end; self.PlaybackState=Enum.PlaybackState.Completed; self.Completed:Fire(Enum.PlaybackState.Completed)
        end)
    end
    function t:Cancel() if co then task.cancel(co) end; self.PlaybackState=Enum.PlaybackState.Cancelled; self.Completed:Fire(Enum.PlaybackState.Cancelled) end
    return strict(t,"Tween")
end})
function banc.client(j)
    return {envoyer=function(_,r,...) assert(r.ClassName=="RemoteEvent"); r.OnServerEvent:Fire(j,...); banc.avancer(0) end,invoquer=function(_,r,...) assert(r.ClassName=="RemoteFunction"); return r.OnServerInvoke(j,...) end,messages=function(_,r) return r._messages[j] or {} end}
end
function banc.fermer_serveur()
    local restants=#fermeture; local limite=maintenant+30
    for _,f in ipairs(fermeture) do task.spawn(function() f(); restants-=1 end) end
    banc.avancer(0)
    while restants>0 and maintenant<limite do banc.avancer(math.min(1,limite-maintenant)) end
    assert(restants==0,"BindToClose : délai fictif de 30 secondes dépassé")
end
function banc.verifier(c,m) assert(c,m or "condition fausse"); print("PASSE : "..(m or "vérification")) end
function banc.egal(a,b,m) banc.verifier(a==b,(m or "égalité").." ("..tostring(a).." / "..tostring(b)..")") end
function banc.proche(a,b,t,m) banc.verifier(math.abs(a-b)<=t,m or "valeurs proches") end
function banc.erreur_attendue(f,m) local ok,e=pcall(f); banc.verifier(not ok and (not m or tostring(e):match(m)~=nil),"erreur attendue : "..(m or "toute erreur")) end
function banc.avertissements() return avertissements end
local osFaux={time=function() return math.floor(epoch+maintenant) end,clock=function() return maintenant end}
function osFaux.time(d)
    if not d then return math.floor(epoch+maintenant) end
    local jours=0
    local function longueur(a) return if a%4==0 and (a%100~=0 or a%400==0) then 366 else 365 end
    if d.year>=1970 then for a=1970,d.year-1 do jours+=longueur(a) end
    else for a=d.year,1969 do jours-=longueur(a) end end
    local mois={31,if longueur(d.year)==366 then 29 else 28,31,30,31,30,31,31,30,31,30,31}
    for m=1,d.month-1 do jours+=mois[m] end
    return (jours+d.day-1)*86400+(d.hour or 12)*3600+(d.min or 0)*60+(d.sec or 0)
end
-- Calendrier grégorien UTC indépendant du fuseau de Windows.
function osFaux.date(format,t)
    format=format or "%c"; t=t or math.floor(epoch+maintenant)
    local jours=math.floor(t/86400); local reste=t-jours*86400; local annee=1970
    local function bissextile(a) return a%4==0 and (a%100~=0 or a%400==0) end
    while jours<0 do annee-=1; jours+=if bissextile(annee) then 366 else 365 end
    while jours>=(if bissextile(annee) then 366 else 365) do jours-=if bissextile(annee) then 366 else 365; annee+=1 end
    local yday=jours+1; local mois=1; local longueurs={31,if bissextile(annee) then 29 else 28,31,30,31,30,31,31,30,31,30,31}
    while jours>=longueurs[mois] do jours-=longueurs[mois]; mois+=1 end
    local d={year=annee,month=mois,day=jours+1,hour=math.floor(reste/3600),min=math.floor(reste/60)%60,sec=reste%60,wday=(math.floor(t/86400)+4)%7+1,yday=yday,isdst=false}
    format=format:gsub("^!",""); if format=="*t" then return d end
    local semaines={"Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"}
    local nomsMois={"January","February","March","April","May","June","July","August","September","October","November","December"}
    local f={Y=string.format("%04d",annee),y=string.format("%02d",annee%100),m=string.format("%02d",mois),d=string.format("%02d",d.day),H=string.format("%02d",d.hour),M=string.format("%02d",d.min),S=string.format("%02d",d.sec),j=string.format("%03d",yday),w=tostring(d.wday-1),['%']='%',A=semaines[d.wday],B=nomsMois[mois],Z="UTC",z="+0000"}
    f.a=f.A:sub(1,3); f.b=f.B:sub(1,3); f.X=f.H..":"..f.M..":"..f.S
    f.x=f.m.."/"..f.d.."/"..f.y; f.c=f.a.." "..f.b.." "..string.format("%2d",d.day).." "..f.X.." "..f.Y
    return (format:gsub("%%(.)",function(k) assert(f[k],"API non simulée : os.date %"..k); return f[k] end))
end
local DateTime={now=function()
    local t=epoch+maintenant
    return strict({_type="DateTime",UnixTimestamp=math.floor(t),UnixTimestampMillis=math.floor(t*1000),ToIsoDate=function() return osFaux.date("!%Y-%m-%dT%H:%M:%S",t).."Z" end},"DateTime")
end}
local environnement={banc=banc,game=game,workspace=services.Workspace,Instance=Instance,task=strict(task,"task"),Vector3=Vector3,Vector2=Vector2,CFrame=strict(CFrame,"CFrame"),Color3=Color3,UDim=UDim,UDim2=strict(UDim2,"UDim2"),TweenInfo=strict(TweenInfo,"TweenInfo"),NumberRange=strict(NumberRange,"NumberRange"),Random=strict(Random,"Random"),Enum=Enum,DateTime=strict(DateTime,"DateTime"),typeof=genre,os=strict(osFaux,"os"),tick=function() return epoch+maintenant end,time=function() return maintenant end,wait=task.wait,spawn=task.spawn,delay=task.delay,warn=function(...) table.insert(avertissements,table.pack(...)) end,shared={}}
for _,n in ipairs({"setmetatable","getmetatable","rawget","rawset","rawequal","rawlen","newproxy","assert","error","pcall","xpcall","pairs","ipairs","next","select","tonumber","tostring","type","unpack","print","math","string","table","coroutine","utf8","bit32","buffer"}) do environnement[n]=natif[n] end
local aleatoire=Random.new(1); environnement.math=table.clone(math)
environnement.math.random=function(a,b) if b then return aleatoire:NextInteger(a,b) elseif a then return aleatoire:NextInteger(1,a) else return aleatoire:NextNumber() end end
environnement.math.randomseed=function(s) aleatoire=Random.new(s) end
function banc.environnement(scriptInstance)
    return setmetatable({script=scriptInstance},{__index=function(_,k) local v=environnement[k]; if v~=nil then return v end; manque("globale "..tostring(k)) end})
end
function banc._installer_require(f) environnement.require=f end
for _,nom in ipairs({"Instance","NumberRange","TweenInfo"}) do environnement[nom]=strict(environnement[nom],nom) end
