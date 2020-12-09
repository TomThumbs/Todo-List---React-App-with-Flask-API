import Paper from "@material-ui/core/Paper";
import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { IconButton, InputBase, Typography } from "@material-ui/core";
import PublishIcon from "@material-ui/icons/Publish";

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
    alignItems: "center",
  },
  iconButton: {
    padding: 10,
  },
}));

export const TodoForm = ({ handleFormChange, handleFormSubmit, userInput }) => {
  const classes = useStyles();

  const handleChange = (event) => {
    handleFormChange(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    handleFormSubmit();
  };

  return (
    <Paper className={classes.paper}>
      <Typography>Todo</Typography>
      <Paper component="form" onSubmit={handleSubmit} method="post">
        <InputBase
          type="text"
          placeholder="New Todo"
          onChange={handleChange}
          value={userInput}
        />
        <IconButton type="submit" className={classes.iconButton}>
          <PublishIcon color="secondary" />
        </IconButton>
      </Paper>
    </Paper>
  );
};
