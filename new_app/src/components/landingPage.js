import React from "react";
import { Link } from "react-router-dom";
import "../css/landingPage.css";

function LandingPage() {
  return (
    <div className="landing-page">
      <div id="welcome">
        <h1>Welcome to the Brain Project!</h1>
        <br />
        <br />
        <br />
        <h2>
          Here you can see all the users,
          <br />
          their snapshots, and parsing results.
        </h2>
      </div>
      <Link to="/users" id="users-press-me">
        <button class="btn aqua-gradient btn-lg">View users</button>
      </Link>
    </div>
  );
}

export default LandingPage;
