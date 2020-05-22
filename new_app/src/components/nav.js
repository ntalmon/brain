import React from "react";
import { Link } from "react-router-dom";
import "../css/nav.css";

class Nav extends React.Component {
  render() {
    return (
      <nav class="navbar navbar-expand-lg navbar-dark elegant-color">
        <Link class="navbar-brand" to="/">
          Brain
        </Link>

        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#basicExampleNav"
          aria-controls="basicExampleNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="basicExampleNav">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
              <Link class="nav-link" to="/">
                Home
                <span class="sr-only">(current)</span>
              </Link>
            </li>
            <li class="nav-item">
              <Link class="nav-link" to="/users">
                Users
              </Link>
            </li>
          </ul>

          <ul class="navbar-nav">
            <li class="nav-item" id="docs-link">
              <a
                class="nav-link"
                href="https://brain.readthedocs.io/en/latest/"
              >
                Docs
              </a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link"
                id="github-link"
                href="https://github.com/noamtau1/brain"
              >
                <i class="fab fa-github fa-2x" id="github-link-icon"></i>
              </a>
            </li>
          </ul>
        </div>
      </nav>
    );
  }
}

export default Nav;
