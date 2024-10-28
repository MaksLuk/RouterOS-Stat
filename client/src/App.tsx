import { useState, useEffect } from 'react';
import {
  VictoryChart,
  VictoryBar,
  VictoryAxis,
  VictoryTheme,
  VictoryLabel
} from 'victory';
import ToggleContent from './components/ToggleContent.tsx';
import BytesOrPacketsButtons from './components/BytesOrPacketsButtons.tsx';
import AllTimeStat from './components/AllTimeStat.tsx';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  const [data, setData] = useState(
    [{name: '-', sended_bytes: 0, sended_packets: 0,
    received_bytes: 0, received_packets: 0,
    tx_bits_per_second: 0, rx_bits_per_second: 0}]
  );
  const [allTimeTx, setAllTimeTx] = useState([{x: '-', y: 0}]);
  const [allTimeRx, setAllTimeRx] = useState([{x: '-', y: 0}]);
  const [allTimeBytes, setAllTimeBytes] = useState<boolean>(true);
  const [txSpeed, setTxSpeed] = useState([{x: '-', y: 0}]);
  const [rxSpeed, setRxSpeed] = useState([{x: '-', y: 0}]);

  const fetchData = async () => {
    const response = await fetch('http://0.0.0.0:8000/api/get_stat');
    const result = await response.json();
    if (!result.success) {
      // при ошибке
    }
    else {
      setData(result.interfaces);
      set_use_states(result.interfaces);
    }
  };

  const handleUpdateAllTimeBytes = (newState: boolean ) => {
    setAllTimeBytes(newState);
    set_use_states(data);
  };

  const set_use_states = (new_data: any[]) => {
    setAllTimeTx(
      new_data.map(
        (item: { name: string; sended_bytes: number; sended_packets: number; }) => ({
        x: item.name,
        y: allTimeBytes ? item.sended_bytes : item.sended_packets
      }))
    );
    setAllTimeRx(
      new_data.map(
        (item: { name: string; received_bytes: number; received_packets: number; }) => ({
        x: item.name,
        y: allTimeBytes ? item.received_bytes : item.received_packets
      }))
    );
    setTxSpeed(
      new_data.map((item: { name: string; tx_bits_per_second: number; }) => ({
        x: item.name,
        y: item.tx_bits_per_second
      }))
    );
    setRxSpeed(
      new_data.map((item: { name: string; rx_bits_per_second: number; }) => ({
        x: item.name,
        y: item.rx_bits_per_second
      }))
    );
  };

  useEffect(() => {
    fetchData();
    const intervalId = setInterval(fetchData, 3000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <>
      <div className="block">
        <h2>Передано данных:</h2>
        <ToggleContent>
          <div className="container-fluid">
            <BytesOrPacketsButtons
              state={allTimeBytes}
              onUpdate={handleUpdateAllTimeBytes}
            />
            <AllTimeStat allTimeTx={allTimeTx} allTimeRx={allTimeRx}/>
          </div>
        </ToggleContent>
      </div>

      <div className="block">
        <h2>Скорость:</h2>
        <ToggleContent>
          <div className="container-fluid">
            <div className="row">

              <div className="col-md-4 col-lg-4 col-xs-12">
                <VictoryChart domainPadding={40} theme={VictoryTheme.material}>
                  <VictoryLabel
                    text="Передача (Tx)"
                    x={180}
                    y={30}
                    textAnchor="middle"
                    style={{ fontSize: 20, fill: "black" }}
                  />
                  <VictoryAxis/>
                  <VictoryAxis dependentAxis tickFormat={(x) => (`${x / 1000}k`)} />
                  <VictoryBar
                    data={txSpeed}
                    labels={({ datum }) => `${datum.y}`}
                  />
                </VictoryChart>
              </div>

              <div className="col-md-4 col-lg-4 col-xs-12">
                <VictoryChart domainPadding={40} theme={VictoryTheme.material}>
                  <VictoryLabel
                    text="Приём (Rx)"
                    x={180}
                    y={30}
                    textAnchor="middle"
                    style={{ fontSize: 20, fill: "black" }}
                  />
                  <VictoryAxis/>
                  <VictoryAxis dependentAxis tickFormat={(x) => (`${x / 1000}k`)} />
                  <VictoryBar
                    data={rxSpeed}
                    labels={({ datum }) => `${datum.y}`}
                  />
                </VictoryChart>
              </div>

            </div>
          </div>
        </ToggleContent>
      </div>

      <div className="block">
        <h2>Интерфейсы</h2>
        <ToggleContent>
          <p>здесь будет таблица</p>
        </ToggleContent>
      </div>
    </>
  )
}

export default App
