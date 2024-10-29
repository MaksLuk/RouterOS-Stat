export type dataType = {
  name: string;
  mac_address: string;
  type: string;
  status: boolean;
  mtu: number;
  actual_mtu: number;
  last_link_up_time: number;
  sended_bytes: number;
  received_bytes: number;
  sended_packets: number;
  received_packets: number;
  tx_bits_per_second: number;
  rx_bits_per_second: number;
  tx_packets_per_second: number;
  rx_packets_per_second: number;
  status_string: string|undefined;  // для таблицы
}

type Props = {
  data: dataType[];
}

const all_keys = [
  ['MAC-адрес', 'mac_address'],
  ['Тип', 'type'],
  ['Статус', 'status_string'],
  ['MTU', 'mtu'],
  ['Текущее MTU', 'actual_mtu'],
  ['Последнее соединение', 'last_link_up_time'],
  ['Отправлено байт*', 'sended_bytes'],
  ['Отправлено пакетов*', 'sended_packets'],
  ['Принято байт*', 'received_packets'],
  ['Принято пакетов*', 'received_packets'],
  ['Скорость приёма (бит/c)', 'tx_bits_per_second'],
  ['Скорость приёма (пакетов/c)', 'tx_packets_per_second'],
  ['Скорость передачи (бит/c)', 'rx_bits_per_second'],
  ['Скорость передачи (пакетов/c)', 'rx_packets_per_second'],
]

function InterfacesTable(props: Props) {
  let data = props.data;
  for (let i = 0; i < data.length; i++) {
    data[i].status_string = data[i].status ? 'Работает' : 'Не работает';
  }

  return (
    <table className='table'>
      <thead>
        <tr>
          <td></td>
          {data.map(i => {
            return <th>{i.name}</th>;
          })}
        </tr>
      </thead>
      <tbody>
        {
          all_keys.map(key => {
            return <tr>
              <th>{key[0]}</th>
              {data.map(i => {
                return <td>{i[key[1]]}</td>;
              })}
            </tr>;
          })
        }
      </tbody>
    </table>
  );
};

export default InterfacesTable;