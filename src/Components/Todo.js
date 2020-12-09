import React from "react";
import { Button, Grid, Paper } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    overflow: "hidden",
    padding: theme.spacing(0, 3),
  },
  paper: {
    maxWidth: 400,
    margin: `${theme.spacing(1)}px auto`,
    padding: theme.spacing(2),
  },
}));

export const Todo = ({ listOfTodos, deleteTodo }) => {
  const classes = useStyles();

  return (
    <Paper outlined="True" className={classes.paper}>
      {listOfTodos.map((todo) => {
        return (
          <Grid container justify="center" key={todo.id} spacing={3}>
            <Grid item xs={4}>
              {todo.content}
            </Grid>
            <Grid item xs={4}>
              {todo.owner}
            </Grid>
            <Grid item xs={4}>
              <Button
                variant="contained"
                color="secondary"
                onClick={() => {
                  deleteTodo(todo.id);
                }}
              >
                Delete
              </Button>
            </Grid>
          </Grid>
        );
      })}{" "}
    </Paper>
  );
};
