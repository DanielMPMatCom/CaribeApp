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


DEFAULT_COLOR_OPTION = "Sin color preferido"


def get_session_acc_amount():
    pass


def get_session_acc_color():
    pass


def get_session_arbitros_amount():
    return st.session_state.get("arbitros_amount", 0)


def get_session_arbitros_color():
    return st.session_state.get("arbitros_color", DEFAULT_COLOR_OPTION)


def get_session_professors_amount():
    return st.session_state.get("professors_amount", 0)


def get_session_professors_color():
    return st.session_state.get("professors_color", DEFAULT_COLOR_OPTION)


def get_session_aaac_amount():
    return st.session_state.get("aaac_amount", 1)


def get_session_aaac_color():
    return st.session_state.get("aaac_color", DEFAULT_COLOR_OPTION)


def get_colors_amount():
    return st.session_state.get("color_rows", 1)


def get_all_session_colors_name():
    return [DEFAULT_COLOR_OPTION] + [
        st.session_state[f"color_name[{i}]"]
        for i in range(get_colors_amount())
        if str(st.session_state.get(f"color_name[{i}]", None)).strip() != ""
    ]


def get_all_session_colors_amount():
    return [None] + [
        st.session_state[f"color_amount[{i}]"]
        for i in range(get_colors_amount())
        if st.session_state.get(f"color_amount[{i}]", None)
    ]


def get_faculty_amount():
    return st.session_state.get("faculty_amount", 1)


def get_all_session_faculties_name():
    return [
        st.session_state[f"faculty_name[{i}]"]
        for i in range(get_faculty_amount())
        if str(st.session_state.get(f"faculty_name[{i}]", "")).strip() != ""
    ]


def get_all_session_faculties_color():
    return [
        st.session_state[f"faculty_color[{i}]"]
        for i in range(get_faculty_amount())
        if st.session_state[f"faculty_color[{i}]", None]
    ]


def get_all_session_faculties_ranking():
    return [
        st.session_state[f"faculty_ranking[{i}]"]
        for i in range(get_faculty_amount())
        if st.session_state.get(f"faculty_ranking[{i}]", None)
    ]


def get_all_session_faculties_athletes():
    return [
        st.session_state[f"faculty_athletes[{i}]"]
        for i in range(get_faculty_amount())
        if st.session_state.get(f"faculty_athletes[{i}]", None)
    ]


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

    with grid_init[0]:

        st.number_input(
            "Cantidad de pullovers para árbitros *",
            key="arbitros_amount",
            min_value=0,
            value=st.session_state.get("arbitros_amount", 0),
        )
        st.selectbox(
            "Color preferido",
            key=f"arbitros_color",
            options=get_all_session_colors_name(),
            disabled=get_all_session_colors_name().__len__() == 1,
            help="Se recomienda añadir los colores primero",
        )
    with grid_init[1]:
        st.number_input(
            "Cantidad de pullovers para maestros *",
            key="professors_amount",
            min_value=0,
            value=st.session_state.get("professors_amount", 0),
        )
        st.selectbox(
            "Color preferido",
            key=f"professors_color",
            options=get_all_session_colors_name(),
            disabled=get_all_session_colors_name().__len__() == 1,
            help="Se recomienda añadir los colores primero",
        )

    with grid_init[2]:

        st.number_input(
            "Cantidad de pullovers para Antiguos Atletas *",
            min_value=0,
            value=st.session_state.get("aaac", 0),
        )
        st.selectbox(
            "Color preferido",
            key=f"input_color_aaac",
            options=get_all_session_colors_name(),
            disabled=get_all_session_colors_name().__len__() == 1,
            help="Se recomienda añadir los colores primero",
        )

    st.divider()

    st.slider(
        "Cantidad de Colores",
        min_value=1,
        max_value=20,
        value=st.session_state.get("color_rows", 1),
        key="color_rows",
    )

    container_colors = st.container()

    def add_row_color(row):
        with container_colors:
            grid = st.columns(2)
            with grid[0]:
                st.text_input(
                    "Color *",
                    key=f"color_name[{row}]",
                )
            with grid[1]:
                st.number_input(
                    "Cantidad de pullovers *",
                    key=f"color_amount[{row}]",
                    min_value=1,
                )
            st.container(height=36, border=0)

    for r in range(get_colors_amount()):
        add_row_color(r)

    st.divider()

    st.slider(
        "Cantidad de facultades",
        min_value=1,
        max_value=30,
        value=st.session_state.get("faculty_rows", 1),
        key="faculty_rows",
    )
    container_faculties = st.container()

    def add_row_faculty(row):
        with container_faculties:
            grid = st.columns(4)
            with grid[0]:
                st.text_input(
                    "Nombre de la Facultad *",
                    key=f"faculty_name[{row}]",
                )
            with grid[1]:
                st.number_input(
                    "Posición en el ranking *",
                    key=f"faculty_ranking[{row}]",
                    min_value=1,
                )
            with grid[2]:
                st.number_input(
                    "Cantidad de atletas",
                    key=f"faculty_athletes[{row}]",
                    min_value=0,
                    help="Se considera que 0 como ausencia de este dato",
                )
            with grid[3]:
                st.selectbox(
                    "Color preferido",
                    key=f"faculty_color[{row}]",
                    options=get_all_session_colors_name(),
                    disabled=get_all_session_colors_name().__len__() == 1,
                    help="Se recomienda añadir los colores primero",
                )
            st.container(height=36, border=0)

    for r in range(get_faculty_amount()):
        add_row_faculty(r)

    def bk_request(container):

        arbitros_amount = get_session_arbitros_amount()
        professors_amount = get_session_professors_amount()
        aaac_amount = get_session_acc_amount()

        colors_name = get_all_session_colors_name()[1:]
        colors_amount = get_colors_amount()[1:]

        faculty_names_array = get_all_session_faculties_name()
        faculty_athletes_array = get_all_session_faculties_athletes()
        faculty_colors_array = get_all_session_faculties_color()
        faculty_rankings_array = get_all_session_faculties_ranking()

        with container:
            if arbitros_amount == 0:
                st.info(
                    "Info: Revise los campos, la cantidad de pullovers seleccionados para los árbitros es 0"
                )
            if professors_amount == 0:
                st.info(
                    "Info: Revise los campos, la cantidad de pullovers seleccionados para los Profesores es 0"
                )
            if aaac_amount == 0:
                st.info(
                    "Info: Revise los campos, la cantidad de pullovers seleccionados para los Antiguos Atletas es 0"
                )

            if len(colors_name) != set(colors_name):
                st.error("Error: Existen colores repetidos")

            if len(colors_name) != get_colors_amount():
                st.error("Error: Faltan datos en las facultades")

            if get_session_arbitros_color() != DEFAULT_COLOR_OPTION:
                color_index = colors_name.index(get_session_arbitros_color())
                amount = colors_amount[color_index]
                if arbitros_amount > amount:
                    st.error(
                        f"Error: La cantidad de pullovers para arbitros ({arbitros_amount}) excede la cantidad de pullovers del color {colors_name[color_index]} ({colors_amount[color_index]})"
                    )
                    return
                colors_amount[color_index] -= arbitros_amount
                arbitros_amount = 0

            if get_session_professors_color() != DEFAULT_COLOR_OPTION:
                color_index = colors_name.index(get_session_professors_color())
                amount = colors_amount[color_index]
                if professors_amount > amount:
                    st.error(
                        f"Error: La cantidad de pullovers para arbitros ({professors_amount}) excede la cantidad de pullovers del color {colors_name[color_index]} ({colors_amount[color_index]})"
                    )
                    return
                colors_amount[color_index] -= professors_amount
                professors_amount = 0

            if get_session_aaac_color() != DEFAULT_COLOR_OPTION:
                color_index = colors_name.index(get_session_aaac_color())
                amount = colors_amount[color_index]
                if aaac_amount > amount:
                    st.error(
                        f"Error: La cantidad de pullovers para arbitros ({aaac_amount}) excede la cantidad de pullovers del color {colors_name[color_index]} ({colors_amount[color_index]})"
                    )
                    return
                colors_amount[color_index] -= aaac_amount
                aaac_amount = 0

            faculty_names = faculty_names_array
            athletes = {}
            ranking = {}
            ranking_inverso = {}
            preferences = {}

            if len(faculty_names) != set(faculty_names):
                st.error("Error: Existen facultades repetidas")

            if len(faculty_names) != get_faculty_amount():
                st.error("Error: Faltan datos en las facultades")

            for i in range(get_faculty_amount()):
                current = faculty_names_array[i]

                if faculty_athletes_array[i] != 0:
                    athletes[current] = faculty_athletes_array[i]

                if faculty_colors_array[i] != DEFAULT_COLOR_OPTION:
                    preferences[current] = faculty_colors_array[i]

                if faculty_rankings_array[i] in ranking_inverso.keys():
                    st.error(
                        f"Error: Facultad {current} y {ranking_inverso[faculty_rankings_array[i]]} tienen el mismo puesto {faculty_rankings_array[i]} en el ranking"
                    )
                    return

            if sorted(faculty_athletes_array)[-1] <= 0:
                st.error(
                    "Error: Es necesario saber la cantidad de atletas de al menos una facultad"
                )
                return

            pullovers = {}

            for i in range(get_colors_amount()):
                pullovers[colors_name[i]] = colors_amount[i]

            try:
                ans = PuLP_Solver(
                    faculties=faculty_names,
                    athletes=athletes,
                    ranking=ranking,
                    available_pullovers=pullovers,
                    pullovers_for_referees=arbitros_amount,
                    pullovers_for_teachers=professors_amount,
                    pullovers_for_aaac=aaac_amount,
                    preferences=preferences,
                )
                print(ans)
                for i in ans.items():
                    st.success(f"{i[0]}: {i[1][0]} Pullovers de Color {i[1][1]}")

            except Exception as e:
                st.error(f"Error: {e}")

    def get_json_content_for_download():

        json_content = st.session_state.to_dict().copy()
        json_content.pop("uploaded_file", None)
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
        file = st.session_state.get("uploaded_file", None)
        if not file:
            st.error("Error al cargar el archivo, por favor vuelva a intentar")
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
