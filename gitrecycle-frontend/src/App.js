import React, { Component, Fragment } from "react";
import Header from "./components/Header";
import Home from "./components/Home";
import Navbar from "./components/Navbar";
class App extends Component {
  render() {
    return (
      <Fragment >
      	<Navbar />
        <Home />
      </Fragment>
    );
  }
}

export default App;