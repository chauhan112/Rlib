import React, { useRef, useEffect, useState } from 'react';

export class ShadowRoot extends React.Component {
    attachShadow(host) {
        if (host == null) {
            return;
        }
        host.attachShadow({ mode: "open" });
        host.shadowRoot.innerHTML = host.innerHTML;
        host.innerHTML = "";
    }

    render() {
        return (
            <span ref={this.attachShadow}>
                {this.props.children}
            </span>
        );
    }
}

const HighlightComponent = ({ value }) => {
    const codeRef = useRef();
    const [css, setCss] = useState(value["css"]);
    const [html, setHTML] = useState({ __html: value["code"] });

    useEffect(() => {
		console.log("should refresh")
        setCss(value["css"]);
        setHTML({ __html: value["code"] });
    }, [value]);

    return (
        <ShadowRoot>
            <style>{css}</style>
            <div dangerouslySetInnerHTML={html} />
        </ShadowRoot>
    );
};

export default HighlightComponent;
