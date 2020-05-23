import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "../css/users-page.css";
import { fetchAPI, showTimestamp } from "../utils";

function UserEntry(props) {
  var [details, setDetails] = useState({ birthday: 0, gender: "" });
  useEffect(() => {
    fetchAPI(`/users/${props.userId}`).then((data) => {
      setDetails({
        birthday: data.birthday,
        gender: data.gender,
      });
    });
  }, []);

  return (
    <tr className="user-entry">
      <td>
        <img src="https://bootdey.com/img/Content/user_1.jpg" alt="" />
        <Link className="user-link" to={`/users/${props.userId}`}>
          {props.username}
        </Link>
      </td>
      <td>{props.userId}</td>
      <td className="text-center">{showTimestamp(details.birthday)}</td>
      <td className="text-center">{details.gender[0]}</td>
    </tr>
  );
}

function UsersPage() {
  var [usersList, setUsersList] = useState([]);
  useEffect(() => {
    fetchAPI("/users").then((data) => {
      setUsersList(data);
    });
  }, []);

  let users = [];
  usersList.forEach((user) => {
    console.log(user);
    users.push(<UserEntry userId={user.user_id} username={user.username} />);
  });
  return (
    <div class="users-page">
      <div className="container bootstrap snippet">
        <div className="row">
          <div className="col-lg-10">
            <div className="main-box no-header clearfix">
              <div className="main-box-body clearfix">
                <div className="table-responsive">
                  <table className="table user-list">
                    <thead>
                      <tr>
                        <th>
                          <span>User</span>
                        </th>
                        <th>
                          <span>ID</span>
                        </th>
                        <th className="text-center">
                          <span>Birthday</span>
                        </th>
                        <th className="text-center">
                          <span>Gender</span>
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
    </div>
  );
}

export default UsersPage;
