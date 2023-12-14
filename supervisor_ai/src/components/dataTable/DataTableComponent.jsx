import DataTable from 'react-data-table-component';
import { customStyles, customTheme } from "./CustomStyles";
const DataTableComponent = (props) => {
    const { columns,data } = props;
    return <>
        <DataTable class="table text-start align-middle table-bordered table-hover mb-0"
            columns={columns}
            data={data}
            pagination
            paginationPerPage={20}
            theme="solarized"
            customStyles={customStyles}
        />    </>
}
export default DataTableComponent;