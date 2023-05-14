import * as React from 'react';
import Chip from '@mui/material/Chip';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';

/**
 * Returns a Concept tag editor
 * @param all_concepts: [[hashtag_id_1, hashtag_1], ...]
 * @param recommended_concepts: [[hashtag_id_1, hashtag_1], ...]
 * @param values: react hook
 * @param setValues: react hook
 * */
export default function ConceptTags(
    all_concepts, recommended_concepts,
    values, setValues) {
    // console.log(values);
    return (
        <Autocomplete
            multiple
            id="tags-filled"
            fullWidth
            options={all_concepts.map((option) => option[1])}
            defaultValue={recommended_concepts}
            // value={values}
            onChange={(event, newValue) => {
                setValues(newValue);
            }}
            freeSolo
            renderTags={(value, getTagProps) =>
                value.map((option, index) => (
                    // eslint-disable-next-line react/jsx-key
                    <Chip variant="outlined" label={option} {...getTagProps({index})} />
                ))
            }
            renderInput={(params) => (
                <TextField
                    {...params}
                    variant="filled"
                    label="Concept hashtags"
                    placeholder="Concept"
                />
            )}
        />
    );
}

