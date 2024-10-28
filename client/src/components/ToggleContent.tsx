import { useState, useRef, ReactNode } from 'react';
import './ToggleContent.css';

interface Props {
  children: ReactNode;
}

function ToggleContent( props: Props ) {
  const [isOpen, setIsOpen] = useState(false);
  const contentRef = useRef(null);

  const toggleContent = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
    <div className="toggle-content">
      <div className="header" onClick={toggleContent}>
        <div className={`triangle ${isOpen ? 'up' : 'down'}`}></div>
      </div>
      <div
        ref={contentRef}
        className={`content ${isOpen ? 'closed' : 'open'}`}
      >
        <hr />
      </div>
      <div
        ref={contentRef}
        className={`content ${isOpen ? 'open' : 'closed'}`}
      >
        {props.children}
      </div>
    </div>
    </>
  )
}

export default ToggleContent;