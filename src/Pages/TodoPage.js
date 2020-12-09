import React, { useState, useEffect } from "react";
import { Todo } from "../Components/Todo";
import { TodoForm } from "../Components/TodoForm";
import { Grid } from "@material-ui/core";

export const TodoPage = () => {
  const [TodoList, setTodoList] = useState([]);
  const [addTodo, setAddTodo] = useState("");

  useEffect(() => {
    fetch("/todolist")
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => {
        setTodoList(data);
      });
  }, []);

  const updateList = () => {
    fetch("/todolist")
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => {
        setTodoList(data);
      });
  };

  const deleteTodo = (id) => {
    fetch(`/todo/${id}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((message) => {
        updateList();
      });
  };

  const handleFormChange = (value) => {
    setAddTodo(value);
  };

  const handleFormSubmit = () => {
    // console.log(addTodo);
    fetch("/todolist", {
      method: "POST",
      body: JSON.stringify({
        content: addTodo,
        owner: "tester",
      }),
      headers: {
        "Content-Type": "application/json; charset=UTF-8",
      },
    })
      .then((response) => response.json())
      .then((message) => {
        setAddTodo("");
        updateList();
      });
  };

  return (
    <Grid container justify="center">
      <Grid item xs={12}>
        <TodoForm
          handleFormChange={handleFormChange}
          handleFormSubmit={handleFormSubmit}
          userInput={addTodo}
        />
      </Grid>
      <Grid item xs={12}>
        <Todo listOfTodos={TodoList} deleteTodo={deleteTodo} />
      </Grid>
    </Grid>
  );
};
