import React, { Component } from "react";
import { Table } from "reactstrap";
import { Button } from "reactstrap";
import { Badge } from "reactstrap";
import BootstrapTable from 'react-bootstrap-table-next';
  
const columns = [{
  dataField: 'id',
  text: 'Product ID'
}, {
  dataField: 'name',
  text: 'Product Name'
}, {
  dataField: 'price',
  text: 'Product Price'
}];
  
const repos = [{
  dataField: 'id',
  text: 'Product ID'
}, {
  dataField: 'name',
  text: 'Product Name'
}, {
  dataField: 'price',
  text: 'Product Price'
}];




export default () =>
  <BootstrapTable keyField='id' data={ repos } columns={ columns } />


