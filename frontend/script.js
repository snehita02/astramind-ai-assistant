// const API="https://astramind-api.onrender.com/api/v1/ask"

// function addUserMessage(text){

// const chat=document.getElementById("chat")

// chat.innerHTML+=`

// <div class="message user">

// <div class="bubble">

// ${text}

// </div>

// </div>

// `

// chat.scrollTop=chat.scrollHeight

// }


// function addAIMessage(data){

// const chat=document.getElementById("chat")

// chat.innerHTML+=`

// <div class="message ai">

// <div class="bubble">

// <b>AstraMind</b>

// <p>${data.answer}</p>

// <div class="meta">

// Confidence: ${data.confidence}<br>

// Grounded: ${data.grounded}<br>

// Evaluation: ${data.evaluation}

// </div>

// </div>

// </div>

// `

// chat.scrollTop=chat.scrollHeight

// }


// async function ask(){

// const query=document.getElementById("query").value

// if(!query) return

// const department=document.getElementById("department").value

// addUserMessage(query)

// document.getElementById("query").value=""

// try{

// const res=await fetch(
// `${API}?query=${encodeURIComponent(query)}&department=${department}&session_id=web-session`
// )

// const data=await res.json()

// addAIMessage(data)

// }catch(e){

// addAIMessage({
// answer:"Could not connect to backend.",
// confidence:"-",
// grounded:"-",
// evaluation:"-"
// })

// }

// }


// document.getElementById("query").addEventListener("keypress",function(event){

// if(event.key==="Enter"){

// ask()

// }

// })




const API="https://astramind-api.onrender.com/api/v1/ask"

let currentChat=[]

function renderHistory(){

const history=JSON.parse(localStorage.getItem("astramind-history"))||[]

const container=document.getElementById("chat-history")

container.innerHTML=""

history.forEach((chat,index)=>{

const item=document.createElement("div")

item.innerText=chat.title

item.onclick=()=>loadChat(index)

container.appendChild(item)

})

}

function saveChat(title){

let history=JSON.parse(localStorage.getItem("astramind-history"))||[]

history.push({title:title,messages:currentChat})

localStorage.setItem("astramind-history",JSON.stringify(history))

renderHistory()

}

function loadChat(index){

const history=JSON.parse(localStorage.getItem("astramind-history"))

currentChat=history[index].messages

renderConversation()

}

function newChat(){

currentChat=[]

document.getElementById("conversation").innerHTML=""

}

function renderConversation(){

const conv=document.getElementById("conversation")

conv.innerHTML=""

currentChat.forEach(m=>{

if(m.type==="question"){

conv.innerHTML+=`
<div class="question">
<b>You:</b> ${m.text}
</div>
`

}

if(m.type==="answer"){

conv.innerHTML+=`
<div class="answer-card">

<b>AstraMind</b>

<p>${m.text}</p>

<div class="meta">

Confidence: ${m.confidence}<br>
Grounded: ${m.grounded}<br>
Evaluation: ${m.evaluation}

</div>

</div>
`

}

})

conv.scrollTop=conv.scrollHeight

}

async function ask(){

const input=document.getElementById("question")

const question=input.value

if(!question) return

const dept=document.getElementById("department").value

currentChat.push({type:"question",text:question})

renderConversation()

input.value=""

try{

const res=await fetch(
`${API}?query=${encodeURIComponent(question)}&department=${dept}&session_id=web-session`
)

const data=await res.json()

currentChat.push({
type:"answer",
text:data.answer,
confidence:data.confidence,
grounded:data.grounded,
evaluation:data.evaluation
})

renderConversation()

saveChat(question.substring(0,30))

}catch(e){

currentChat.push({
type:"answer",
text:"Error connecting to backend.",
confidence:"-",
grounded:"-",
evaluation:"-"
})

renderConversation()

}

}

document.getElementById("question").addEventListener("keypress",function(e){

if(e.key==="Enter"){
ask()
}

})

renderHistory()