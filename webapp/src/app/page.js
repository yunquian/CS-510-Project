'use client';

// import * as React from 'react';
import Image from 'next/image'
import styles from './page.module.css'
// import Button from '@material-ui/core/Button'
// import TextField from '@material-ui/core/TextField'
import Button from '@mui/material/Button'
import {Checkbox, FormControlLabel, TextField} from "@mui/material";
import {useEffect, useState} from "react";
import ReactDOM, {render} from 'react-dom';

import {Autocomplete} from "./autocomplete";
import ConceptTags from "@/app/hashtag-concept-input";

// async function handleSubmit() {
//     // let response = await fetch('/api/' + currentTable, {
//     //   method: 'POST', headers: {
//     //     'Content-Type': 'application/json'
//     //   },
//     //   body: JSON.stringify(inst)
//     // });
//     // let jsonValue = await response.json();
//     // if (response.ok) {
//     //   openAlertDialog('Success');
//     //   clearContent();
//     // } else {
//     //   openAlertDialog(jsonValue);
//     // }
// }
//

export default function Home() {
    // Hashtag submissions
    const [staticHashtags, setStaticHashtags] = useState({});
    const [concepts, setConcepts] = useState([]);
    useEffect(() => {
        console.log(concepts);
        console.log(staticHashtags);
    }, [concepts]);
    // Page content input
    const [highlightInput, setHighlightInput] = useState('');
    const handleHighlightChange = event => {
        setHighlightInput(event.target.value);
    };
    const [contentInput, setContentInput] = useState('');
    const handleContentChange = event => {
        setContentInput(event.target.value);
    };
    const handleUploadContent = async event => {
        let response = await fetch('/api/hashtags', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                content: contentInput,
                highlight: highlightInput
            })

        });
        let children = []
        let jsonValue = await response.json();
        let initialStaticHashtagState = {};
        for (let groupName in jsonValue.static) {
            for (let item of jsonValue.static[groupName]) {
                initialStaticHashtagState[item[0]] = false;
            }
        }
        setStaticHashtags(initialStaticHashtagState);

        for (let groupName in jsonValue.static) {
            children.push(<p>{groupName}</p>)
            for (let item of jsonValue.static[groupName]) {
                children.push(
                    // <p>{item[1]}</p>
                    <FormControlLabel
                        control={<Checkbox
                            onClick={() => setStaticHashtags(
                                prevState => ({...prevState, [item[0]]: !prevState[item[0]]}))}
                        />}
                        label={item[1]}/>
                );
            }
        }
        ReactDOM.render(children,
            document.getElementById('static-hashtags'));
        // concepts
        let recommendedConcepts = jsonValue.recommend.map((option) => option[1]);
        setConcepts(oldConcepts => [...oldConcepts, ...recommendedConcepts]);
        ReactDOM.render([ConceptTags(jsonValue.concepts, recommendedConcepts, concepts, setConcepts)],
            document.getElementById('concept-hashtags'));
    };


    const handleSubmit = async event => {
        let response = await fetch('/api/submit', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                hashtag: {
                    concepts: concepts,
                    static_hashtag_selected_states: staticHashtags
                }
            })
        });
    };

    return (
        <main className={styles.main}>
            <div>
                <p>
                    CDL hashtag submission demo
                </p>
            </div>
            <TextField
                id="text-highlight"
                label="Highlighted Text"
                multiline
                maxRows={2}
                fullWidth
                margin="normal"
                value={highlightInput}
                onChange={handleHighlightChange}
            />
            <TextField
                id="text-content"
                label="Webpage Content"
                // placeholder="Placeholder"
                multiline
                minRows={5}
                maxRows={12}
                fullWidth
                margin="normal"
                value={contentInput}
                onChange={handleContentChange}
            />

            <Button variant="outlined" onClick={handleUploadContent}>
                Retrieve and suggest Hashtags
            </Button>

            <div id='static-hashtags'></div>

            <div id='concept-hashtags' style={{width: "100%"}} width={'100%'}></div>

            <Button variant="contained" onClick={handleSubmit}>Submit</Button>

        </main>
    )
}
