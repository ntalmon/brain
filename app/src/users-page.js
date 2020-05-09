import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./users-page.css";
import fetchAPI from "./utils";

function UserInList(props) {
  var firstLastName = props.userName.split(" ");
  var initials = firstLastName[0][0] + firstLastName[1][0];
  var userId = props.userId;
  return (
    <tr>
      <td>
        <div className="userImage">{initials}</div>
        <Link to={"/users/" + userId} class="user-link">
          {props.userName}
        </Link>
      </td>
      <td>
        <span>{props.userId}</span>
      </td>
    </tr>
  );
}

function Users() {
  var [usersList, setUsersList] = useState([]);
  useEffect(() => {
    fetchAPI("/users").then((data) => {
      setUsersList(data);
    });
  }, []);

  let users = [];
  usersList.forEach((user) => {
    users.push(<UserInList userId={user.user_id} userName={user.username} />);
  });
  return (
    <div class="container bootstrap snippet">
      <div class="row">
        <div class="col-lg-12">
          <div class="main-box no-header clearfix">
            <div class="main-box-body clearfix">
              <div class="table-responsive">
                <table class="table user-list">
                  <thead>
                    <tr>
                      <th>
                        <span>User</span>
                      </th>
                      <th>
                        <span>User ID</span>
                      </th>
                    </tr>
                  </thead>
                  <tbody>{users}</tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Users;
