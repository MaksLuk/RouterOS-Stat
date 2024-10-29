import { useState, useEffect } from 'react';
import ToggleContent from './components/ToggleContent.tsx';
import BytesOrPacketsButtons from './components/BytesOrPacketsButtons.tsx';
import AllTimeStat from './components/AllTimeStat.tsx';
import SpeedStat from './components/SpeedStat.tsx';
import InterfacesTable, { dataType } from './components/InterfacesTable.tsx';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  const [data, setData] = useState<dataType[]>([]);
  const [allTimeBytes, setAllTimeBytes] = useState<boolean>(true);
  const [speedBytes, setSpeedBytes] = useState<boolean>(true);

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

  const getSpeedTxData = () => {
    return data.map((item) => ({
      x: item.name,
      y: speedBytes ? item.tx_bits_per_second : item.tx_packets_per_second,
    }));
  };

  const getSpeedRxData = () => {
    return data.map((item) => ({
      x: item.name,
      y: speedBytes ? item.rx_bits_per_second : item.rx_packets_per_second,
    }));
  };

  const handleUpdateAllTimeBytes = (newState: boolean ) => {
    setAllTimeBytes(newState);
  };

  const handleUpdateSppedBytes = (newState: boolean ) => {
    setSpeedBytes(newState);
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
            <AllTimeStat txData={getAllTimeTxData()} rxData={getAllTimeRxData()}/>
          </div>
        </ToggleContent>
      </div>

      <div className="block">
        <h2>Скорость:</h2>
        <ToggleContent>
          <div className="container-fluid">
            <BytesOrPacketsButtons
              state={speedBytes}
              onUpdate={handleUpdateSppedBytes}
            />
            <SpeedStat txData={getSpeedTxData()} rxData={getSpeedRxData()} />
          </div>
        </ToggleContent>
      </div>

      <div className="block">
        <h2>Интерфейсы</h2>
        <ToggleContent>
          <InterfacesTable data={data} />
        </ToggleContent>
      </div>
    </>
  )
}

export default App
