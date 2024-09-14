import streamlit as st
from PuLP_Solver import PuLP_Solver
import json


class GenericInputData:
    def __init__(
        self,
        *,
        name,
        value,
        error,
        type_input,
        required,
        ## text, numeric, options
    ) -> None:
        self.name = name
        self.value = value
        self.error = error
        self.type_input = type_input
        self.required = required


class GenericBaseClass:
    def __init__(self) -> None:
        self.data: "list[GenericInputData]" = []

    def update_value(self, index, new_value):
        self.data[index] = new_value

    def get_values(self):
        return self.data


class FacultyData(GenericBaseClass):
    def __init__(self) -> None:
        GenericBaseClass.__init__(self)
        self.data = [
            "",
            0,
            0,
            "",
        ]


class ColorData(GenericBaseClass):
    def __init__(self) -> None:
        GenericBaseClass.__init__(self)
        self.data = ["", 0]


colors_data_storage: "list[ColorData]" = []
faculty_data_storage: "list[FacultyData]" = []


def main():

    stc = st.columns(4)
    with stc[0]:
        st.title("Caribe Demo")

    with stc[1]:
        st.image(
            "./src/indio.png",
            caption="",
            width=90,
        )

    st.divider()

    grid_init = st.columns(3, gap="medium")
    colores_options = ["Sin color preferido"] + [
        v.data[0] for v in colors_data_storage if v.data[0] != "" and v.data
    ]
    with grid_init[0]:

        arbitros = st.number_input(
            "Cantidad de pullovers para árbitros *",
            key='arbitros',
            min_value=0,
            value=st.session_state.get("arbitros", 0),
        )
        arbitros_colors = st.selectbox(
            "Color preferido",
            key=f"input_color_arb",
            options=colores_options,
            disabled=colores_options.__len__() == 1,
            help="Se recomienda añadir los colores primero",
        )
    with grid_init[1]:
        professors = st.number_input(
            "Cantidad de pullovers para maestros *",
            min_value=0,
        )
        profesors_colors = st.selectbox(
            "Color preferido",
            key=f"input_color_prof",
            options=colores_options,
            disabled=colores_options.__len__() == 1,
            help="Se recomienda añadir los colores primero",
        )

    with grid_init[2]:

        aacc = st.number_input(
            "Cantidad de pullovers para Antiguos Atletas *",
            min_value=0,
            value=st.session_state.get("aacc", 0),
        )
        aacc_colors = st.selectbox(
            "Color preferido",
            key=f"input_color_aacc",
            options=colores_options,
            disabled=colores_options.__len__() == 1,
            help="Se recomienda añadir los colores primero",
        )

    st.divider()

    color_rows = st.slider(
        "Cantidad de Colores",
        min_value=1,
        max_value=20,
        value=1,
    )

    container_colors = st.container()

    def add_row_color(row):
        with container_colors:
            grid = st.columns(2)
            with grid[0]:
                colors_data_storage[r].data[0] = st.text_input(
                    "Color *",
                    key=f"input_expense_color_{row}",
                )
            with grid[1]:
                colors_data_storage[r].data[1] = st.number_input(
                    "Cantidad de pullovers *",
                    key=f"input_amount_color_{row}",
                    min_value=1,
                )
            st.container(height=36, border=0)

    for r in range(color_rows):
        if colors_data_storage.__len__() <= r:
            colors_data_storage.append(ColorData())
        add_row_color(r)

    st.divider()

    num_rows_faculties = st.slider(
        "Cantidad de facultades", min_value=1, max_value=30, value=1
    )
    container_faculties = st.container()

    def add_row_faculty(row):
        with container_faculties:
            grid = st.columns(4)
            with grid[0]:
                faculty_data_storage[r].data[0] = st.text_input(
                    "Nombre de la Facultad *",
                    key=f"input_expense_faculty_{row}",
                )
            with grid[1]:
                faculty_data_storage[r].data[1] = st.number_input(
                    "Posición en el ranking *",
                    key=f"input_amount_faculty_{row}",
                    min_value=1,
                )
            with grid[2]:
                faculty_data_storage[r].data[2] = st.number_input(
                    "Cantidad de atletas",
                    key=f"input_athletes_faculty_{row}",
                    min_value=0,
                    help="Se considera que 0 como ausencia de este dato",
                )
            with grid[3]:
                faculty_data_storage[r].data[3] = st.selectbox(
                    "Color preferido",
                    key=f"input_color_faculty_{row}",
                    options=colores_options,
                    disabled=colores_options.__len__() == 1,
                    help="Se recomienda añadir los colores primero",
                )
            st.container(height=36, border=0)

    for r in range(num_rows_faculties):
        if faculty_data_storage.__len__() <= r:
            faculty_data_storage.append(FacultyData())
        add_row_faculty(r)

    def bk_request(container):

        with container:
            if arbitros == 0:
                st.info(
                    "Info: Revise los campos, la cantidad de pullovers seleccionados para los árbitros es 0"
                )
            if aacc == 0:
                st.info(
                    "Info: Revise los campos, la cantidad de pullovers seleccionados para los Antiguos Atletas es 0"
                )

            nombre_de_las_facultades = []
            athletes = {}
            ranking = {}
            ranking_inverso = {}
            preferences = {}
            some_faculty_has_athlete = False

            for i in faculty_data_storage:
                if i.data[0] == "":
                    st.error("Error: Faltan datos en las facultades")
                    return
                nombre_de_las_facultades.append(i.data[0])

                if i.data[2] != 0:
                    athletes[i.data[0]] = i.data[2]

                if i.data[3] != "Sin color preferido":
                    preferences[i.data[0]] = i.data[3]

                if i.data[1] in ranking_inverso.keys():
                    st.error(
                        f"Error: Facultad {i.data[0]} y {ranking_inverso[i.data[1]]} tienen el puesto {i.data[1]} el ranking"
                    )
                    return
                ranking[i.data[0]] = i.data[1]
                if i.data[2] != 0:
                    some_faculty_has_athlete = True

            if not some_faculty_has_athlete:
                st.error(
                    "Error: Es necesario saber la cantidad de atletas de al menos una facultad"
                )
                return

            pullovers = {}

            for i in colors_data_storage:
                if i.data[0] == "" or not i.data[0]:
                    st.error("Error: Faltan datos en los colores")
                    return

                pullovers[i.data[0]] = i.data[1]

            if aacc != 0 and aacc_colors != "Sin color preferido":
                pullovers[aacc_colors] -= aacc
                if pullovers[aacc_colors] < 0:
                    st.error(
                        f"Error: No hay suficientes pullovers de color {aacc_colors} para los Antiguos Atletas"
                    )
                    return

            if arbitros != 0 and arbitros_colors != "Sin color preferido":
                pullovers[arbitros_colors] -= arbitros
                if pullovers[arbitros_colors] < 0:
                    st.error(
                        f"Error: No hay suficientes pullovers de color {arbitros_colors} para los Árbitros y Maestros"
                    )
                    return

            try:
                ans = PuLP_Solver(
                    faculties=nombre_de_las_facultades,
                    athletes=athletes,
                    ranking=ranking,
                    available_pullovers=pullovers,
                    pullovers_for_referees_and_teachers=arbitros,
                    pullovers_for_aaac=aacc,
                    preferences=preferences,
                )
                print(ans)
                for i in ans.items():
                    st.success(f"{i[0]}: {i[1][0]} Pullovers de Color {i[1][1]}")

            except Exception as e:
                st.error(f"Error: {e}")

    def get_json_content_for_download():

        json_content = st.session_state.to_dict().copy()
        json_content.pop("uploaded_file")
        binary_data = json.dumps(json_content).encode("utf-8")
        return binary_data

    st.button(
        "Ejecutar", on_click=lambda: bk_request(end_container), use_container_width=True
    )
    st.download_button(
        label="Descargar Datos Introducidos",
        data=get_json_content_for_download(),
        file_name="resultados.json",
        mime="text/csv",
        use_container_width=True,
    )

    def set_json_file_data():
        file = st.session_state["uploaded_file"]
        json_from_binary = json.loads(file.read())
        st.write("Archivo caribeño cargado:")
        st.write(json_from_binary)
        st.session_state.update(json_from_binary)

    file = st.file_uploader(
        label="Cargar Datos desde un archivo caribeño",
        # on_change=set_json_file_data,
        type=["json"],
        key="uploaded_file",
        on_change=set_json_file_data,
    )

    st.write(st.session_state)

    end_container = st.container()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Caribe Demo",
        page_icon=":",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main()
