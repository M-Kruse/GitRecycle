import React, { useState } from 'react';
import logo from '../assets/img/GitRecycle-Logo-128.png'; // with import
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

const Example = (props) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggle = () => setIsOpen(!isOpen);

  return (
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
              <NavLink href="">Queries</NavLink>
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
    </div>
  );
}

export default Example;
