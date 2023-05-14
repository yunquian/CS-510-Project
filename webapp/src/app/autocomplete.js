import React from 'react';
import { createAutocomplete } from '@algolia/autocomplete-core';
import { parseAlgoliaHitHighlight } from '@algolia/autocomplete-preset-algolia';

// @ts-ignore
function useAutocomplete(props) {
    const [state, setState] = React.useState(() => ({
        collections: [],
        completion: null,
        context: {},
        isOpen: false,
        query: '',
        activeItemId: null,
        status: 'idle',
    }));

    const autocomplete = React.useMemo(
        () =>
            createAutocomplete({
                ...props,
                onStateChange(params) {
                    props.onStateChange?.(params);
                    setState(params.state);
                },
            }),
        []
    );

    return { autocomplete, state };
}

// @ts-ignore
export function Autocomplete(props) {
    const { autocomplete, state } = useAutocomplete({
        ...props,
        id: 'hashtag-autocomplete',
        defaultActiveItemId: 0,
    });
    const inputRef = React.useRef(null);


    return (
        <div {...autocomplete.getRootProps({})}>
            <div className="box">
                <div className="box-body">
                    <div className="box-compose">
                        <form
                            {...autocomplete.getFormProps({
                                inputElement: inputRef.current,
                            })}
                        >
                            <textarea
                                className="box-textbox"
                                ref={inputRef}
                                {...autocomplete.getInputProps({
                                    inputElement: inputRef.current,
                                    autoFocus: true,
                                    maxLength: 280,
                                })}
                            />
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}



function AccountItem({ hit }) {
    return (
        <div className="account-body">
            <div className="account-avatar">
                <img src={hit.image} alt="" />
            </div>
            <div>
                <div className="account-name">
                    <Highlight hit={hit} attribute="name" />
                </div>
                <div className="account-handle">
                    @<Highlight hit={hit} attribute="handle" />
                </div>
            </div>
        </div>
    );
}

function Highlight({ hit, attribute }) {
    return (
        <>
            {parseAlgoliaHitHighlight({
                hit,
                attribute,
            }).map(({ value, isHighlighted }, index) => {
                if (isHighlighted) {
                    return (
                        <mark key={index} className="account-highlighted">
                            {value}
                        </mark>
                    );
                }

                return <React.Fragment key={index}>{value}</React.Fragment>;
            })}
        </>
    );
}