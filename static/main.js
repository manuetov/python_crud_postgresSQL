const userForm = document.querySelector("#userForm")

// variables globales //////////////
let users = []
let editing = false
// para el metodo put-edit
let userId = null
// para el metodo put-edit
//  ////////////////////////////////

window.addEventListener("DOMContentLoaded", async () => {
   // lo primero que se ejecuta cuando la página carga
   const res = await fetch("/api/users");
   // trae todos los datos
   const data = await res.json()
   // se convierten a formato json
   users = data
   // se guarda en el array
   renderUsers(users)
   // llama a la funcion y le pasa [users]como parametro
   })

userForm.addEventListener("submit", async (e) => {
   e.preventDefault();
   // evita que se refresque la pantalla

   const username = userForm["username"].value
   const email = userForm["email"].value
   const password = userForm["password"].value
   // guardo los valores de los inputs del formulario

   if (!editing) {
   // si no se está editando, se esta creando método POST
      const response = await fetch("/api/users", {
      // fetch enviamos los datos del formulario al backend 
         method: "POST",
         headers: {
            "Content-Type": "application/json",
         // con el metodo post en formato json
         },
         body: JSON.stringify({
            // username: username,
            username,
            email,
            password
         })
      })            
      const data = await response.json()
      // covierto la respuesta en json           
      users.unshift(data)   
      // se guardan en el array al inicio. con push se añade al final
      renderUsers(users) 
      }  else { 
      // //////////// método PUT /////////////////
         const res = await fetch(`/api/users/${userId}`, {
            method: "PUT",
            headers: {
               "Content-Type": "application/json"
            },
            body: JSON.stringify({
               username,
               email,
               password
            })
         })
         const updatedUser = await res.json()
         // usamos la variable global userId que contiene data.id
         console.log("data")

         users = users.map(user => user.id === updatedUser.id ? updatedUser : user)
         // si el user.id es igual al updatedUser significa que hay una coincidencia
         // y se genera un nuevo array con el nuevo usuario o el anterior sino coincide 
         renderUsers(users)
         editing = false
         userId = null
      }
      userForm.reset()
})

function renderUsers(users){
   const userList = document.querySelector("#userList")
   // seleccion el #userList del index.html
   userList.innerHTML = ""
   // con innerHTML "" => limpia el userList

   users.forEach(user => {
      const userItem = document.createElement("li")
      // con createElement crea un elemneto html tipo lista en cada iteración,
      // además al ser un elemento, podremos usar otros tipos de selectores, como: querySelector
      userItem.classList = "list-group-item list-group-item-dark my-2"
      userItem.innerHTML = `
         <header class="d-flex justify-content-between align-items-center">
            <h3>${user.username}</h3>
            <div class="d-flex flex-column ">
               <button class="btn-delete btn btn-danger btn-sm">Borrar</button>
               <button class="btn-edit btn btn-secondary mt-2 btn-sm">Editar</button>
            </div>
         </header>
         <p>${user.email}</p>  
      `
      // ///////////////////// btnDelete ///////////////////////
      const btnDelete = userItem.querySelector(".btn-delete")
      // selecciono el boton por us clase .btn-delete
      btnDelete.addEventListener("click", async () => {
         // evento de escucha click al botón
         // console.log(user.id)
         const res = await fetch(`/api/users/${user.id}`, {
            method: "DELETE"
         })
         const data = await res.json()
         
         users = users.filter(user => user.id !== data.id)
         // con filter quita del array el usuario eliminado
         renderUsers(users)
         // renderiza nuevamente con array sin el usuario eliminado
      })

      userList.appendChild(userItem)
      // appendChild añado userItem a userList
      // console.log(userItem)

      // ///////////////////// btnEdit ///////////////////////   
      const btnEdit = userItem.querySelector(".btn-edit")

      btnEdit.addEventListener("click", async (e) => {
         // console.log(user.id)
         const res = await fetch(`/api/users/${user.id}`)
         const data = await res.json()

         userForm["username"].value = data.username
         userForm["email"].value = data.email
         // relleno los campos del form con los datos traidos 
         
         editing = true;
         userId = data.id

      })
   })

}
