import React, { Component } from "react";
import logo from '../assets/img/GitRecycle-Logo.png'; // with import

class Header extends Component {
  render() {
    return (
      <div className="text-center">
        <img
          alt="GitRecycleLogo"
          src={logo}
          width="300"
          className="img-thumbnail"
          style={{ marginTop: "20px" }}
        />
        <hr />
        <h5>
          <i>All your mistake are belong to me</i>
        </h5>
        <h1>GitRecycle</h1>
      </div>
    );
  }
}

export default Header;