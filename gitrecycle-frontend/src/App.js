import React, { Component, useState } from 'react';
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
  UncontrolledDropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  NavbarText
} from 'reactstrap';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import Home from "./components/Home";
import RepoList from "./components/RepoList";
import QueryList from "./components/QueryList";
import logo from './assets/img/GitRecycle-Logo-128.png'; // with import

const RouterApp = (props) => {

  const [isOpen, setIsOpen] = useState(false);

  const toggle = () => setIsOpen(!isOpen);

    return (
    <Router>
            <div>
      <Navbar color="light" light expand="md">
        <img
          alt="GitRecycleLogo"
          src={logo}
          width="64"
          />
        <NavbarBrand href="/">GitRecycle</NavbarBrand>
        <NavbarToggler onClick={toggle} />
        <Collapse isOpen={isOpen} navbar>
          <Nav className="mr-auto" navbar>
          <NavItem>
              <NavLink href="/dashboard">Dashboard</NavLink>
            </NavItem>
            <NavItem>
              <NavLink href="/queries">Queries</NavLink>
            </NavItem>
            <UncontrolledDropdown nav inNavbar>
              <DropdownToggle nav caret href="/">
                Repos
              </DropdownToggle>
              <DropdownMenu right>
                <DropdownItem>
                <NavLink href="/repos/">
                All
                </NavLink>
                </DropdownItem>
                <DropdownItem>
                <NavLink href="/repos/missing">Missing</NavLink>
                </DropdownItem>
                
                <DropdownItem>
                  <NavLink href="/repos/stale">Stale</NavLink>
                </DropdownItem>
              </DropdownMenu>
            </UncontrolledDropdown>
          </Nav>
          <NavbarText>
          <i>All your mistake are belong to me</i>
          </NavbarText>
        </Collapse>
      </Navbar>
          <hr />
          <Switch>
              <Route exact path='/' component={Home} />
              <Route exact path='/repos/' component={RepoList} />
              <Route exact path='/repos/missing/' component={RepoList} />
              <Route exact path='/queries/' component={QueryList} />
          </Switch>
        </div>
      </Router>
    );
  }



export default RouterApp;
