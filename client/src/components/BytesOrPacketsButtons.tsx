function BytesOrPacketsButtons({state, onUpdate}) {
  return (
    <div className="btn-group" role="group" aria-label="Basic example">
      <button
        type="button"
        className={`btn btn- ${state === true ? 'active' : ''}`}
        onClick={() => onUpdate(true)}
      >
        Байты
      </button>
      <button
        type="button"
        className={`btn ${state === false ? 'active' : ''}`}
        onClick={() => onUpdate(false)}
      >
        Пакеты
      </button>
    </div>
  );
};

export default BytesOrPacketsButtons;