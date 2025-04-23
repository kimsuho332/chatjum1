from PyQt5 import uic, QtWidgets, QtGui
import sys
import os
import dropbox
from dropbox.exceptions import ApiError

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # 동적 경로 설정 (EXE 루트 경로)
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)  # EXE 경로
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))  # PY 경로

        ui_path = os.path.join(base_path, "main.ui")
        if not os.path.exists(ui_path):
            self.show_error(f"{ui_path} 파일을 찾을 수 없습니다.")
            sys.exit(1)
        uic.loadUi(ui_path, self)
        self.setWindowTitle("잭슨 탈곡기")
        self.setWindowIcon(QtGui.QIcon(os.path.join(base_path, "icon.ico")))

        self.access_token = "sl.u.AFkFR-vwv_49ivtXaTICy81cwj9WDDAQyPM2b5ZD1Wu6biceW-L0-6BUz05E2Vp3gofaPUM3GNmicV2b3DznHG1oVSZ-pqBJXkcOHAI36QOpU-6vV18A62TR-ItTVizH3BXSREIw0-GIsy-nwTuFgyTLZfFD0MPm5pDGGpbRc9WyDywFjLJb88PWwdPNGqyHRQl_vqv6EG7YABf1hKSh01jNnKT8SmxH6PJNQVMAvP99WyW--IPnM-x3iwo3l-24ZslCKQBJ8JVTWKRRqwZBJc7nna_LyK2p3clfjX16fTRmRLyEgnDzQOIZ0ihlgFEbj_KBoYTI_nC4Qa6GNH7u0Aj1APO1nb_HcCo_ssxtaVegDBWOx1sLfFkvyvy7xceAVenyEsjHRgTi01hZTW9no7QCnvRb4AuVOvvfztTLIjSmba06EaJW_MaJTu78dFq134TYmRD0RyNeMWO0u_-rd49CDh2wRopcyG94e6mnExeAqT4WDH8iCo-xf11SMzJwDfzIH08IE8a8z1NaURH8nLxyPw-z4zYU5MHPdg-pgPvV-DTmzwn9cK9xhmWCRX9ydDBiy81UU72iRVmMstFGG9IxAWUcm9Bo0V597kuWT5h07Ju9FiraxC4aqRu2wErbRb3rhAETtXX9-DG3VCSN-KndTaFyzoSNzOnFpY8lrbLKtrhkFrgvJeJx4lXYhSVfxKX6aW596yNxYF0ZGFo1frqhmPPyjopGTa9vndI4mdYkJwl9LfpkKsaJ0TK_UfkP0-Rpx4ND6mdZPc28uYGaBqfRX27Zp4WjJ_8B0ACTYLE_1nxhA8IPK04GmHUMnsU90q3JLGsqhhr2W7eJmtUUgBOd7r_9geOwV64VLL2eQYgXPuB5XJfU6-mp1LMWkptHWMxZZ1zSd-wK-HQaFLvc8mts-PWTAwRTWGXKX_uePJjr-RtsPtubWZF1mSrvOOUDUyfhmPLkLxnj6g3CpOcbklYp-KMHyEdxw2vQz41nU4Rn-1QFLq2LMaPjnvQ3EM2pCEtSAXcbFIanWTJND0zuY94C3dfqmCCFzbtLLDY1p8HZC3-67mH8aiPGixYndVqOVxxvt8_m2LrUPzwIp58qZ6Z0g7ny17jl7DWv362zXbV3nGU7ZrX5iOCqfPty0Y6-bNsg9Wkq-Ut3b7MJwtdvLgidK_FsEo__7gbBEtjxvICP3PJU4s8S-pKfrrF0tZLCCgsbidyR1_dFmqi565kWZxe8L0C7624YzuQm6tsPJyC3GuAjbEgfVHSsf0PhejV6gcHTllpUDwRPgY4EP1fcLUNOs9r4lDo9KA7rpGwM7psJT3EPLSfFIhszRjjfQIr0bdHkF9gGrr15BybpPHrYIkvs0Mnc4brAHuHM6qADS-kjJ5Ic9zs_aYxUIanVhN6N1n2tryy24BT_L5oev1KnRMb9rSJLIgvflgsFf8-LgfZ2Fg"  # 네 토큰 넣어
        self.dbx = dropbox.Dropbox(self.access_token)

        self.logoLabel = self.findChild(QtWidgets.QLabel, "logoLabel")
        if not self.logoLabel:
            self.show_error("logoLabel을 찾을 수 없습니다.")
            sys.exit(1)
        self.logoLabel.setPixmap(QtGui.QPixmap(os.path.join(base_path, "logo.png")))
        self.logoLabel.show()

        self.weekendButton = self.findChild(QtWidgets.QPushButton, "weekendButton")
        self.weekdayButton = self.findChild(QtWidgets.QPushButton, "weekdayButton")
        self.backButton = self.findChild(QtWidgets.QPushButton, "backButton")

        if not all([self.weekendButton, self.weekdayButton, self.backButton]):
            self.show_error("main.ui에서 버튼을 찾을 수 없습니다.")
            sys.exit(1)

        self.weekendButton.clicked.connect(lambda: self.show_grade_screen("weekend"))
        self.weekdayButton.clicked.connect(lambda: self.show_grade_screen("weekday"))
        self.backButton.clicked.connect(self.back_to_main)
        self.backButton.hide()

    def show_error(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("오류")
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def download_file(self, filename):
        try:
            metadata, res = self.dbx.files_download(f"/{filename}")
            return res.content.decode('utf-8')
        except ApiError as e:
            self.show_error(f"Dropbox에서 {filename} 다운로드 실패: {e}")
            return None

    def upload_file(self, filename, content):
        try:
            self.dbx.files_upload(content.encode('utf-8'), f"/{filename}", mode=dropbox.files.WriteMode.overwrite)
        except ApiError as e:
            self.show_error(f"Dropbox에 {filename} 업로드 실패: {e}")

    def show_grade_screen(self, group_type):
        base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_path, "grade.ui")
        if not os.path.exists(ui_path):
            self.show_error(f"{ui_path} 파일을 찾을 수 없습니다.")
            sys.exit(1)
        self.group_type = group_type
        self.centralWidget().hide()
        self.logoLabel.hide()
        self.grade_widget = uic.loadUi(ui_path)
        self.setCentralWidget(self.grade_widget)
        self.setWindowTitle("잭슨 탈곡기")
        self.grade_widget.grade1Button.clicked.connect(lambda: self.show_next_screen("중1"))
        self.grade_widget.grade2Button.clicked.connect(lambda: self.show_next_screen("중2"))
        self.grade_widget.grade3Button.clicked.connect(lambda: self.show_next_screen("중3"))
        self.grade_widget.backButton.clicked.connect(self.back_to_main)
        self.grade_widget.backButton.show()

    def show_next_screen(self, grade):
        base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_path, "student_list.ui")
        if not os.path.exists(ui_path):
            self.show_error(f"{ui_path} 파일을 찾을 수 없습니다.")
            sys.exit(1)
        self.grade = grade
        self.centralWidget().hide()
        self.logoLabel.hide()
        self.student_widget = uic.loadUi(ui_path)
        self.setCentralWidget(self.student_widget)

        student_entries = self.load_students(self.group_type, self.grade)
        if not student_entries:
            self.show_error(f"{self.group_type} - {self.grade}에 학생이 없습니다.")
            self.back_to_grade()
            return

        scroll_content = self.student_widget.findChild(QtWidgets.QWidget, "scrollAreaWidgetContents")
        if not scroll_content:
            scroll_content = self.student_widget.findChild(QtWidgets.QWidget, "studentWidget")
            if not scroll_content:
                self.show_error("scrollAreaWidgetContents 또는 studentWidget을 찾을 수 없습니다.")
                self.back_to_grade()
                return

        layout = scroll_content.layout() if scroll_content.layout() else QtWidgets.QVBoxLayout(scroll_content)
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        self.student_buttons = []
        for date, name in student_entries:
            display_text = f"{date} {name}"
            btn = QtWidgets.QPushButton(display_text)
            btn.setFixedSize(400, 80)
            btn.clicked.connect(lambda checked, dt=display_text: self.show_scoring_screen(dt))
            layout.addWidget(btn)
            self.student_buttons.append(btn)
        self.student_widget.backButton.clicked.connect(self.back_to_grade)

    def load_students(self, group_type, grade):
        content = self.download_file("scores.txt")
        if not content:
            return []
        student_entries = []
        for line in content.splitlines():
            parts = line.strip().split(":")
            if len(parts) >= 5 and parts[2] == group_type and parts[3] == grade:
                student_entries.append((parts[0], parts[1]))
        student_entries.sort(reverse=True)
        return student_entries

    def show_scoring_screen(self, display_text):
        base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_path, "scoring.ui")
        if not os.path.exists(ui_path):
            self.show_error(f"{ui_path} 파일을 찾을 수 없습니다.")
            sys.exit(1)
        self.display_text = display_text
        self.student_name = display_text.split(" ")[1]
        self.centralWidget().hide()
        self.logoLabel.hide()
        self.scoring_widget = uic.loadUi(ui_path)
        self.setCentralWidget(self.scoring_widget)
        self.setWindowTitle("잭슨 탈곡기")

        student_name_label = self.scoring_widget.findChild(QtWidgets.QLabel, "studentNameLabel")
        if not student_name_label:
            self.show_error("studentNameLabel을 찾을 수 없습니다.")
            self.back_to_students()
            return
        student_name_label.setText(display_text)

        self.correct_answers = self.load_answers(display_text)
        if not self.correct_answers:
            self.show_error(f"{display_text}의 데이터를 찾을 수 없습니다.")
            self.back_to_students()
            return

        problem_count = len(self.correct_answers)
        self.input_fields = []
        answer_widget = self.scoring_widget.findChild(QtWidgets.QWidget, "answerWidget")
        if not answer_widget:
            self.show_error("answerWidget을 찾을 수 없습니다.")
            self.back_to_students()
            return

        layout = answer_widget.layout()
        if not layout:
            layout = QtWidgets.QGridLayout(answer_widget)
        else:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        for i in range(problem_count):
            row = i // 5
            col = i % 5 * 2
            problem_label = QtWidgets.QLabel(f"문제 {i+1}:")
            line_edit = QtWidgets.QLineEdit()
            line_edit.setPlaceholderText("답 입력")
            line_edit.setFixedSize(60, 40)
            layout.addWidget(problem_label, row, col)
            layout.addWidget(line_edit, row, col + 1)
            self.input_fields.append(line_edit)

        self.result_label = self.scoring_widget.findChild(QtWidgets.QLabel, "resultLabel")
        if not self.result_label:
            self.show_error("resultLabel을 찾을 수 없습니다.")
            self.back_to_students()
            return
        self.result_label.setText("결과: ")

        self.scoring_widget.calculateButton.clicked.connect(self.check_answers)
        self.scoring_widget.backButton.clicked.connect(self.back_to_students)

    def load_answers(self, display_text):
        content = self.download_file("scores.txt")
        if not content:
            return None
        date, name = display_text.split(" ", 1)
        for line in content.splitlines():
            parts = line.strip().split(":")
            if len(parts) >= 5 and parts[0] == date and parts[1] == name:
                return parts[4].split("/")
        return None

    def check_answers(self):
        wrong_problems = []
        for i, field in enumerate(self.input_fields):
            user_answer = field.text().strip()
            correct_answer = self.correct_answers[i].strip()
            if user_answer != correct_answer:
                wrong_problems.append(i + 1)
        result_text = f"틀린 문제: {', '.join(map(str, wrong_problems))}" if wrong_problems else "모두 정답!"
        self.result_label.setText(f"결과: {result_text}")

        date, name = self.display_text.split(" ", 1)
        result_entry = f"{date}:{name}:{self.group_type}:{self.grade}:{','.join(map(str, wrong_problems)) if wrong_problems else '없음'}\n"
        try:
            content = self.download_file("results.txt") or ""
            content += result_entry
            self.upload_file("results.txt", content)
        except Exception as e:
            self.show_error(f"Dropbox에 결과 저장 실패: {e}")

    def back_to_students(self):
        self.show_next_screen(self.grade)

    def back_to_grade(self):
        self.centralWidget().hide()
        self.logoLabel.hide()
        self.show_grade_screen(self.group_type)

    def back_to_main(self):
        base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_path, "main.ui")
        if not os.path.exists(ui_path):
            self.show_error(f"{ui_path} 파일을 찾을 수 없습니다.")
            sys.exit(1)
        self.centralWidget().hide()
        uic.loadUi(ui_path, self)
        self.setWindowTitle("잭슨 탈곡기")
        self.logoLabel = self.findChild(QtWidgets.QLabel, "logoLabel")
        if not self.logoLabel:
            self.show_error("logoLabel을 찾을 수 없습니다 (back)")
            sys.exit(1)
        self.logoLabel.setPixmap(QtGui.QPixmap(os.path.join(base_path, "logo.png")))
        self.logoLabel.show()
        self.weekendButton = self.findChild(QtWidgets.QPushButton, "weekendButton")
        self.weekdayButton = self.findChild(QtWidgets.QPushButton, "weekdayButton")
        self.backButton = self.findChild(QtWidgets.QPushButton, "backButton")
        if not all([self.weekendButton, self.weekdayButton, self.backButton]):
            self.show_error("main.ui에서 버튼을 찾을 수 없습니다 (back)")
            sys.exit(1)
        self.weekendButton.clicked.connect(lambda: self.show_grade_screen("weekend"))
        self.weekdayButton.clicked.connect(lambda: self.show_grade_screen("weekday"))
        self.backButton.clicked.connect(self.back_to_main)
        self.backButton.hide()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())