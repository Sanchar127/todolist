<template>
  <div id="app" class="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-lg">
    <div class="header text-center mb-8">
      <h1 class="text-3xl font-semibold text-gray-800 mb-4">Todo List</h1>
      <input
        v-model="newTask"
        @keyup.enter="addTodo"
        placeholder="Add a new task"
        class="w-full p-3 text-lg border-2 border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
    </div>
    <h2 class="text-xl font-semibold text-gray-700 mb-4">Incomplete Tasks</h2>
    <ul class="todo-list space-y-4">
      <li
        v-for="todo in incompleteTodos"
        :key="todo.id"
        class="todo-item flex justify-between items-center p-4 bg-gray-50 rounded-lg shadow-sm transition hover:bg-gray-100"
      >
        <span :class="{ 'line-through text-gray-400': todo.completed }" class="todo-text text-lg text-gray-700">
          {{ todo.task }}
        </span>
        <div class="buttons flex gap-4">
          <button
            @click="toggleComplete(todo.id)"
            class="btn-complete py-2 px-4 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none"
          >
            {{ todo.completed ? 'Undo' : 'Complete' }}
          </button>
          <button
            @click="deleteTodo(todo.id)"
            class="btn-delete py-2 px-4 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none"
          >
            Deletes
          </button>
        </div>
      </li>
    </ul>

    <h2 class="text-xl font-semibold text-gray-700 mt-8 mb-4">Completed Tasks</h2>
    <ul class="todo-list space-y-4">
      <li
        v-for="todo in completedTodos"
        :key="todo.id"
        class="todo-item flex justify-between items-center p-4 bg-gray-50 rounded-lg shadow-sm transition hover:bg-gray-100"
      >
        <span :class="{ 'line-through text-gray-400': todo.completed }" class="todo-text text-lg text-gray-700">
          {{ todo.task }}
        </span>
        <div class="buttons flex gap-4">
          <button
            @click="toggleComplete(todo.id)"
            class="btn-complete py-2 px-4 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none"
          >
            {{ todo.completed ? 'Undo' : 'Complete' }}
          </button>
          <button
            @click="deleteTodo(todo.id)"
            class="btn-delete py-2 px-4 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none"
          >
            Delete
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      todos: [],
      newTask: "",
    };
  },
  mounted() {
    this.fetchTodos();
  },
  computed: {
    // Filter incomplete tasks
    incompleteTodos() {
      return this.todos.filter(todo => !todo.completed);
    },
    // Filter completed tasks
    completedTodos() {
      return this.todos.filter(todo => todo.completed);
    },
  },
  methods: {
    async fetchTodos() {
      try {
        const response = await axios.get("http://localhost:8000/todos");
        this.todos = response.data;
      } catch (error) {
        console.error("Error fetching todos:", error);
      }
    },
    async addTodo() {
      if (this.newTask.trim()) {
        const newTodo = {  task: this.newTask, completed: false };
        try {
          const response = await axios.post("http://localhost:8000/todos", newTodo);
          this.todos.push(response.data);
          this.newTask = ""; // Reset the input field
        } catch (error) {
          console.error("Error adding todo:", error);
        }
      }
    },
    async toggleComplete(todoId) {
      const todo = this.todos.find(t => t.id === todoId);
      if (todo) {
        todo.completed = !todo.completed;
        try {
          await axios.put(`http://localhost:8000/todos/${todoId}`, todo);
        } catch (error) {
          console.error("Error updating todo:", error);
        }
      }
    },
    async deleteTodo(todoId) {
      try {
        await axios.delete(`http://localhost:8000/todos/${todoId}`);
        this.todos = this.todos.filter(todo => todo.id !== todoId);
      } catch (error) {
        console.error("Error deleting todo:", error);
      }
    },
  },
};
</script>

<style scoped>
/* Tailwind styles are applied directly in the template, no need for additional custom styles here */
</style>
