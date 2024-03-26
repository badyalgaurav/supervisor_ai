
import  { createTheme } from 'react-data-table-component';
// createTheme creates a new theme named solarized that overrides the build in dark theme
const customTheme =createTheme('solarized', {
    text: {
        primary: '#FFFFFF',
        secondary: '#FFFFFF',
    },
    background: {
        default: '#191C24 !important',
    },
    context: {
        background: '#cb4b16',
        text: '#FFFFFF',
    },
    divider: {
        default: 'black',
    },
    action: {
        button: 'rgba(0,0,0,.54)',
        hover: 'rgba(0,0,0,.08)',
        disabled: 'rgba(0,0,0,.12)',
    },
}, 'dark');

//  Internally, customStyles will deep merges your customStyles with the default styling.
const customStyles = {
    rows: {
        style: {
            minHeight: '48px', // override the row height
        },
    },
    headCells: {
        style: {
            paddingLeft: '8px', // override the cell padding for head cells
            paddingRight: '8px',
            fontSize: "medium"
        },
    },
    cells: {
        style: {
            paddingLeft: '8px',
            paddingRight: '8px',
        },
    },
};

export { customStyles, customTheme };