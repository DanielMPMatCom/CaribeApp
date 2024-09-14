import streamlit as st
from PuLP_Solver import PuLP_Solver
import json
import requests


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
    return st.session_state.get("aaac_amount", 0)


def get_session_acc_color():
    return st.session_state.get("aaac_color", DEFAULT_COLOR_OPTION)


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
        if str(st.session_state.get(f"color_name[{i}]", "")).strip() != ""
    ]


def get_all_session_colors_amount():
    return [None] + [
        st.session_state[f"color_amount[{i}]"]
        for i in range(get_colors_amount())
        if st.session_state.get(f"color_amount[{i}]", None)
    ]


def get_faculty_amount():
    return st.session_state.get("faculty_rows", 1)


def get_all_session_faculties_name():
    return [
        st.session_state[f"faculty_name[{i}]"]
        for i in range(get_faculty_amount())
        if str(st.session_state.get(f"faculty_name[{i}]", "")).strip() != ""
    ]


def get_all_session_faculties_color():
    return [
        st.session_state[f"faculty_color[{i}]"] for i in range(get_faculty_amount())
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


def get_chat_id(token, username):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print(data)
        for result in data["result"]:
            if "message" in result and "chat" in result["message"]:
                chat = result["message"]["chat"]
                if chat.get("username") == username:
                    print(chat["id"])
                    return chat["id"]
    else:
        raise Exception(f"{response.status_code}-{response.text}")


def send_telegram_message(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"{response}-{response.text}")

    return response


def main():

    stc = st.columns(4)
    with stc[0]:
        st.title("Caribe")

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
            index=get_all_session_colors_name().index(
                st.session_state.get("arbitros_color", DEFAULT_COLOR_OPTION)
            ),
        )
    with grid_init[1]:
        st.number_input(
            "Cantidad de pullovers para los profesores *",
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
            index=get_all_session_colors_name().index(
                st.session_state.get("professors_color", DEFAULT_COLOR_OPTION)
            ),
        )

    with grid_init[2]:

        st.number_input(
            "Cantidad de pullovers para Antiguos Atletas *",
            min_value=0,
            key="aaac_amount",
            value=st.session_state.get("aaac_amount", 0),
        )
        st.selectbox(
            "Color preferido",
            key=f"aaac_color",
            options=get_all_session_colors_name(),
            disabled=get_all_session_colors_name().__len__() == 1,
            help="Se recomienda añadir los colores primero",
            index=get_all_session_colors_name().index(
                st.session_state.get("aaac_color", DEFAULT_COLOR_OPTION)
            ),
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
                    index=get_all_session_colors_name().index(
                        st.session_state.get(
                            f"faculty_color[{row}]", DEFAULT_COLOR_OPTION
                        )
                    ),
                )
            st.container(height=36, border=0)

    for r in range(get_faculty_amount()):
        add_row_faculty(r)

    def bk_request(container):

        arbitros_amount = get_session_arbitros_amount()
        professors_amount = get_session_professors_amount()
        aaac_amount = get_session_acc_amount()

        colors_name = get_all_session_colors_name()[1:]
        colors_amount = get_all_session_colors_amount()[1:]

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

            if len(colors_name) != get_colors_amount():
                st.error("Error: Faltan datos en los colores")
                return

            if len(colors_name) != len(set(colors_name)):
                st.error("Error: Existen colores repetidos")
                return

            if get_session_arbitros_color() != DEFAULT_COLOR_OPTION:
                color_index = colors_name.index(get_session_arbitros_color())
                amount = colors_amount[color_index]
                if arbitros_amount > amount:
                    st.error(
                        f"Error: La cantidad de pullovers para arbitros ({arbitros_amount}) excede la cantidad de pullovers del color {colors_name[color_index]} ({colors_amount[color_index]})"
                    )
                    return

            if get_session_professors_color() != DEFAULT_COLOR_OPTION:
                color_index = colors_name.index(get_session_professors_color())
                amount = colors_amount[color_index]
                if professors_amount > amount:
                    st.error(
                        f"Error: La cantidad de pullovers para arbitros ({professors_amount}) excede la cantidad de pullovers del color {colors_name[color_index]} ({colors_amount[color_index]})"
                    )
                    return

            if get_session_aaac_color() != DEFAULT_COLOR_OPTION:
                color_index = colors_name.index(get_session_aaac_color())
                amount = colors_amount[color_index]
                if aaac_amount > amount:
                    st.error(
                        f"Error: La cantidad de pullovers para arbitros ({aaac_amount}) excede la cantidad de pullovers del color {colors_name[color_index]} ({colors_amount[color_index]})"
                    )
                    return

            faculty_names = faculty_names_array
            athletes = {}
            ranking = {}
            ranking_inverso = {}
            preferences = {}

            if len(faculty_names) != get_faculty_amount():
                st.error("Error: Faltan datos en las facultades")
                return

            if len(faculty_names) != len(set(faculty_names)):
                st.error("Error: Existen facultades repetidas")
                return

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
                else:
                    ranking[current] = faculty_rankings_array[i]
                    ranking_inverso[faculty_rankings_array[i]] = ranking[current]

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
                    color_for_referees=get_session_arbitros_color(),
                    color_for_teachers=get_session_professors_color(),
                    color_for_aaac=get_session_aaac_color(),
                    preferences=preferences,
                )

                st.session_state["solution_for_request"] = ans
            except Exception as e:
                st.error(f"Error: {e}")

    def get_json_content_for_download():
        json_content = st.session_state.to_dict().copy()
        json_content.pop("uploaded_file", None)
        json_content.pop("user_telegram", None)
        binary_data = json.dumps(json_content).encode("utf-8")
        return binary_data

    st.download_button(
        label="Descargar Datos Introducidos",
        data=get_json_content_for_download(),
        file_name="resultados.json",
        mime="application/json",
        use_container_width=True,
    )

    def set_json_file_data(container):
        file = st.session_state.get("uploaded_file", None)
        if not file:
            with container:
                st.error("Error al cargar el archivo, por favor vuelva a intentar")
            return
        try:
            json_from_binary = json.loads(file.read())
            st.session_state.update(json_from_binary)
        except Exception as e:
            with container:
                st.error(
                    f"Error al cargar el archivo, por favor vuelva a intentar: {e}"
                )

    st.file_uploader(
        label="Cargar Datos desde un archivo caribeño",
        type=["json"],
        key="uploaded_file",
        on_change=lambda: set_json_file_data(end_container),
    )

    def indio_attack(container):
        message = st.session_state.get("solution_for_request", None)

        username = st.session_state.get("user_telegram", None)

        if not message:
            with container:
                st.error(
                    "Parece que no hay datos que enviar, no arriesgue al indio en un viaje por gusto"
                )
            return

        if not username:
            with container:
                st.error(
                    "El indio no ha recibido el destinatario, por favor revise el nombre de usuario"
                )
            return

        if str(username).startswith("@"):
            username = username[1:]
        print("hey there. Im batman")
        try:
            chat_id = get_chat_id(st.secrets["TELEGRAM_BOT_TOKEN"], username)
            if not chat_id:
                with container:
                    st.error(
                        "Parece que aun no has hablado con el indio, confirma que lo conoces https://t.me/el_indio_de_los_caribe_bot"
                    )
            send_telegram_message(st.secrets["TELEGRAM_BOT_TOKEN"], chat_id, message)
        except Exception as e:
            with container:
                st.error(
                    f"Lo sentimos, parece que el indio se perdió, confirme que si @ de telegram sea el correcto, o la conexión {e}"
                )

    st.chat_input(
        placeholder="https://t.me/el_indio_de_los_caribe_bot",
        key="user_telegram",
        on_submit=lambda: indio_attack(container=end_container),
        # disabled=(st.session_state.get("solution_for_request", None) == None),
    )

    end_container = st.container()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Caribe App",
        page_icon=":",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    main()
