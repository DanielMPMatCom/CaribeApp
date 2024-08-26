import streamlit as st
from PuLP_Solver import PuLP_Solver


def execute_text():
    assignation = PuLP_Solver(
        ["ISRI", "MATCOM", "DER", "TUR"],
        {"ISRI": 80, "MATCOM": 80, "DER": 20, "TUR": 50},
        {"ISRI": 1, "MATCOM": 2, "DER": 3, "TUR": 5},
        {"A": 100, "B": 100, "C": 100},
        50,
        30,
        {"ISRI": "A", "MATCOM": "B", "DER": "B", "TUR": "C"},
    )

    for faculty, (pullovers, color) in assignation.items():
        print(f"{faculty}: {pullovers} pullovers color {color}")
        st.info(f"{faculty}: {pullovers} pullovers color {color}")


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
        self.data: list[GenericInputData] = []

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


colors_data_storage: list[ColorData] = []
faculty_data_storage: list[FacultyData] = []


def main():

    st.title("Caribe Demo")
    st.divider()
    st.text("Pullovers")
    gridinit = st.columns(2)
    with gridinit[0]:
        arbitros = st.number_input(
            "Cantidad de colores para árbitros y maestros *", min_value=0
        )
    with gridinit[1]:
        aacc = st.number_input(
            "Cantidad de colores para Antiguos Atletas *", min_value=0
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
                colores = ["Sin color preferido"] + [
                    v.data[0] for v in colors_data_storage if v.data[0] != "" and v.data
                ]

                faculty_data_storage[r].data[3] = st.selectbox(
                    "Color preferido",
                    key=f"input_color_faculty_{row}",
                    options=colores,
                    disabled=colores.__len__() == 1,
                    help="Se recomienda añadir los colores primero",
                )
            st.container(height=36, border=0)

    for r in range(num_rows_faculties):
        if faculty_data_storage.__len__() <= r:
            faculty_data_storage.append(FacultyData())
        add_row_faculty(r)

    def testing():
        st.error(arbitros)
        st.error(aacc)

        for i in faculty_data_storage:
            st.info(i.get_values())

        for i in colors_data_storage:
            st.success(i.get_values())

    container_colors = st.container()

    st.button("Execute", on_click=testing)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Caribe Demo",
        # page_icon=":green_book:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main()
