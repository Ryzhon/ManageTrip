import { createStore } from 'vuex'
import UserModule from "./user.module.js"
import TodoModule from "./todo.module.js"
import TripModule from "./trip.module.js"

export default createStore({
modules:{
    user: UserModule,
    todo: TodoModule,
    trip: TripModule
}

})