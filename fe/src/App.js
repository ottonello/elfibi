import React from 'react';
import './App.css';
import Plot from 'react-plotly.js';
import Button from 'react-bootstrap/Button';
import DatePicker from "react-datepicker";

import "react-datepicker/dist/react-datepicker.css";

class App extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            data: [
                {
                    x: [1, 2, 3],
                    y: [2, 6, 3],
                    type: 'columns',
                    mode: 'lines+markers',
                    marker: {color: 'red'},
                }
            ],
            startDate: new Date()
        }
        console.log("YES")
    }

    handleChange(event) {
        let formatted_date = this.state.startDate.getFullYear() + "-" + (this.state.startDate.getMonth() + 1) + "-" + this.state.startDate.getDate()
        fetch("http://localhost:8000/api/heart/" + formatted_date)
            .then(response => {
                if (response.status === 200) {
                    return response.json()
                } else  if (response.status === 401) {
                    window.location = "http://localhost:8080/auth";
                }
            })
            .then(json => {
                console.log(json)
                var dataset = json["activities-heart-intraday"].dataset
                var x = dataset.map((ds) => ds.time)
                var y = dataset.map((ds) => ds.value)
                var new_data = [
                    {
                        x: x,
                        y: y,
                        type: 'columns',
                        mode: 'lines+markers',
                        marker: {color: 'red'},
                    }
                ]

                this.setState({data: new_data})

            })
            .catch(function (error) {
                    console.log(error)
                    // window.location = "http://localhost:8080/auth";
                }
            );
    }

    render() {
        return (
            <div className="App">
                <Plot
                    data={this.state.data}
                    layout={{title: 'Your heart rate'}}
                    style={{width: "100%", height: "100%"}}
                />

                <Button variant="primary" onClick={(e) => this.handleChange(e)}>Fetch those heart beats</Button>{' '}
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
