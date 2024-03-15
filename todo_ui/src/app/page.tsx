import Image from "next/image";
import TodoList from "./components/TodoList";

export default async function Home() {
    
//   async function getTodoList() {
// var todolList1 = await fetch("http://localhost:3000/api/getTodoList");
// const res1 = await todolList1.json();
// }
  return (
    <div>
      <TodoList/>
    </div>
  );
}
