from pathlib import Path
import optuna.visualization as vis


class OptunaVisualizer:
    def __init__(self, study, algorithm):
        self.study = study
        self.algorithm = algorithm


    def _save_plot(self, figure, filename):
        
        report_path = Path("artifacts")/"tuning_visualization"/self.algorithm/filename

        report_path.parent.mkdir(parents=True, exist_ok=True)

        figure.write_html(report_path)


    def optimization_history(self):

        figure = vis.plot_optimization_history(self.study)

        self._save_plot(figure,"optimization_history.html")
    

    def parameter_importance(self):

        figure = vis.plot_param_importances(self.study)

        self._save_plot(figure,"parameter_importance.html")

    def slice_plot(self):

        figure = vis.plot_slice(self.study)

        self._save_plot(figure,"slice_plot.html")

    def parallel_coordinate(self):

        figure = vis.plot_parallel_coordinate(self.study)

        self._save_plot(figure, "parallel_coordinate.html")

    def contour_plot(self):

        figure = vis.plot_contour(self.study)

        self._save_plot(
            figure,
            "contour_plot.html"
        )

    def generate_all(self):

        self.optimization_history()
        self.parameter_importance()
        self.slice_plot()
        self.parallel_coordinate()
        self.contour_plot()


