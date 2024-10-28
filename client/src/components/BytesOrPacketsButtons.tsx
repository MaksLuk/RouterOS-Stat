import { useState } from 'react';

type Props = {
  state: boolean;
  onUpdate: (newState: boolean) => void;
}

function BytesOrPacketsButtons(props: Props) {
  const [state, setState] = useState<boolean>(props.state);

  const handleClick = (newState: boolean) => {
    setState(newState);
    props.onUpdate(newState);
  };

  return (
    <div className="btn-group" role="group" aria-label="Basic example">
      <button
        type="button"
        className={`btn btn- ${state === true ? 'active' : ''}`}
        onClick={() => handleClick(true)}
      >
        Байты
      </button>
      <button
        type="button"
        className={`btn ${state === false ? 'active' : ''}`}
        onClick={() => handleClick(false)}
      >
        Пакеты
      </button>
    </div>
  );
};

export default BytesOrPacketsButtons;