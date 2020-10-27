import React from 'react';
import './App.css';
import Plot from 'react-plotly.js';
import Button from 'react-bootstrap/Button';
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";
import {Overlay, Spinner} from "react-bootstrap";

class App extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            startDate: new Date(),
            data: [],
            layout: {title: 'Your heart rate', yaxis: {fixedrange: true}, xaxis: {tickformat: "%H~%M~%S"}},
            frames: [],
            config: {}
        }
        this.target = React.createRef()
    }

    handleChange(event) {
        let formatted_date = this.state.startDate.getFullYear() + "-" + (this.state.startDate.getMonth() + 1) + "-" + this.state.startDate.getDate()
        fetch("http://localhost:8000/api/heart/" + formatted_date)
            .then(response => {
                if (response.status === 200) {
                    return response.json()
                } else if (response.status === 401) {
                    window.location = "http://localhost:8080/auth";
                }
            })
            .then(json => {
                console.log(json)
                var dataset = json.dataset
                var x = dataset.map((ds) => ds.time)
                var y = dataset.map((ds) => ds.value)
                var new_data = [
                    {
                        x: x,
                        y: y,
                        type: 'scatter',
                        mode: 'lines+markers',
                        marker: {color: 'red'},
                    }
                ]

                this.setState({data: new_data})

            })
            .catch(function (error) {
                    console.log(error)
                }
            ).finally((info) => this.setState({show: false}));
    }

    render() {
        return (
            <div className="App">
                <Plot
                    data={this.state.data}
                    layout={this.state.layout}
                    style={{width: "100%", height: "100%"}}
                    frames={this.state.frames}
                    config={this.state.config}
                />
                <Overlay target={this.target.current} show={this.state.show} placement="left">
                    {({placement, arrowProps, show: _show, popper, ...props}) => (
                        <div
                            {...props}
                            style={{
                                backgroundColor: 'rgba(255, 100, 100, 0.85)',
                                padding: '2px 10px',
                                color: 'white',
                                borderRadius: 3,
                                ...props.style,
                            }}
                        >
                            <Spinner animation="border" role="status">
                                <span className="sr-only">Loading...</span>
                            </Spinner>
                        </div>
                    )}
                </Overlay>
                <Button variant="primary"
                        ref={this.target} onClick={(e) => {
                    this.handleChange(e);
                    this.setState({show: true})
                }}>Fetch those heart beats</Button>{' '}
                <DatePicker
                    selected={this.state.startDate}
                    onChange={date => this.setState({startDate: date})}
                />
                <p>{this.state.startDate.toString()}</p>
            </div>
        );
    }
}

export default App;
