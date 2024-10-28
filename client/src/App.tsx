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
  const [allTimeBytes, setAllTimeBytes] = useState<boolean>(true);

  const fetchData = async () => {
    const response = await fetch('http://0.0.0.0:8000/api/get_stat');
    const result = await response.json();
    if (!result.success) {
      // при ошибке
    }
    else {
      setData(result.interfaces);
    }
  };

  const handleUpdateAllTimeBytes = (newState: boolean ) => {
    setAllTimeBytes(newState);
  };

  useEffect
  (() => {
    fetchData();
    const intervalId = setInterval(fetchData, 3000);
    return () => clearInterval(intervalId);
  }, []);

  useEffect(() => {}, [allTimeBytes]);

  const getAllTimeTxData = () => {
    return data.map((item) => ({
      x: item.name,
      y: allTimeBytes ? item.sended_bytes : item.sended_packets,
    }));
  };

  const getAllTimeRxData = () => {
    return data.map((item) => ({
      x: item.name,
      y: allTimeBytes ? item.received_bytes : item.received_packets,
    }));
  };

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
            <AllTimeStat allTimeTx={getAllTimeTxData()} allTimeRx={getAllTimeRxData()}/>
          </div>
        </ToggleContent>
      </div>

      <div className="block">
        <h2>Скорость:</h2>
        <ToggleContent>
          <div className="container-fluid">
            <div className="row">

              <div className="col-md-4 col-lg-4 col-xs-12">
              </div>

              <div className="col-md-4 col-lg-4 col-xs-12">
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
