import {
    VictoryChart,
    VictoryBar,
    VictoryAxis,
    VictoryTheme,
    VictoryStack,
    VictoryLabel
  } from 'victory';

type Props = {
  txData: {x: string, y: number}[];
  rxData: {x: string, y: number}[];
}

function AllTimeStat(props: Props) {
  return (
    <div className="row">
      <div className="col-md-4 col-lg-4 col-xs-12">
        <VictoryChart domainPadding={40} theme={VictoryTheme.material}>
          <VictoryLabel
            text="Всего"
            x={180}
            y={30}
            textAnchor="middle"
            style={{ fontSize: 20, fill: "black" }}
          />
          <VictoryAxis/>
          <VictoryAxis dependentAxis tickFormat={(x) => (`${x / 1000}k`)} />
          <VictoryStack>
            <VictoryBar data={props.txData} />
            <VictoryBar data={props.rxData} />
          </VictoryStack>
        </VictoryChart>
      </div>

      <div className="col-md-4 col-lg-4 col-xs-12">
        <VictoryChart domainPadding={40} theme={VictoryTheme.material}>
          <VictoryLabel
            text="Передано (Tx)"
            x={180}
            y={30}
            textAnchor="middle"
            style={{ fontSize: 20, fill: "black" }}
          />
          <VictoryAxis/>
          <VictoryAxis dependentAxis tickFormat={(x) => (`${x / 1000}k`)} />
          <VictoryBar
            data={props.txData}
            labels={({ datum }) => `${datum.y}`}
          />
        </VictoryChart>
      </div>

      <div className="col-md-4 col-lg-4 col-xs-12">
        <VictoryChart domainPadding={40} theme={VictoryTheme.material}>
          <VictoryLabel
            text="Принято (Rx)"
            x={180}
            y={30}
            textAnchor="middle"
            style={{ fontSize: 20, fill: "black" }}
          />
          <VictoryAxis/>
          <VictoryAxis dependentAxis tickFormat={(x) => (`${x / 1000}k`)} />
          <VictoryBar
            data={props.rxData}
            labels={({ datum }) => `${datum.y}`}
          />
        </VictoryChart>
      </div>
    </div>
  );
};

export default AllTimeStat;