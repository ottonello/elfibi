import React from 'react';
import './App.css';
import Plot from 'react-plotly.js';
import Button from 'react-bootstrap/Button';

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
                },
                {type: 'lines', x: [1, 2, 3], y: [2, 5, 3]},
            ]
        }
        console.log("YES")
    }

    handleChange(event) {
        console.log("GRACIAS PELOTUDO")
        fetch("http://localhost:8000/api/heart/today")
            .then(response => response.json())
            .then(json => {
                var new_data = json.get("activities-heart-intraday")
                this.setState({data: new_data})
            })
            .catch(function (error) {
                // window.location = "http://localhost:8080/auth";
            }
        );
    }

    render() {
        return (
            <div className="App">
                <Plot
                    data={this.state.data}
                    layout={{title: 'A Fancy Plot'}}
                    style={{width: "100%", height: "100%"}}
                />
                <Button variant="primary" onClick={(e) => this.handleChange(e)}>Fetch those heart beats</Button>{' '}

            </div>
        );
    }
}

export default App;
