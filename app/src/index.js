import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";
import "./index.css";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Users from "./users-page";
import UserPage from "./user-page";

function Index() {
  return <Users />;
}

const Home = () => {
  return <span></span>;
};

function App() {
  return (
    <Router>
      <div className="App">
        <Switch>
          <Route path="/" exact component={Index} />
          <Route path="/users" exact component={Users} />
          <Route path="/users/:id" component={UserPage} />
        </Switch>
      </div>
    </Router>
  );
}

ReactDOM.render(<App />, document.getElementById("root"));
