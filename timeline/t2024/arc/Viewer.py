from useful.FileDatabase import File
from basic import Main as ObjMaker
def PlotterModel():
    import matplotlib.pyplot as plt
    colors = ['#000000', '#1E93FF', '#F93C31', '#4FCC30', '#FFDC00',
              '#999999', '#E53AA3', '#FF851B', '#87D8F1', '#921231', '#555555']
    colormap = plt.matplotlib.colors.ListedColormap(colors)
    fileLoc = '../06_Jun/.arc-prize-2024/arc-agi_training_challenges.json'
    data = None
    def show_train_pair(train, save_path=None, task_id=None):
        """
        Show the input-output pair of a training task
        train: list of dict, each dict contains 'input' and 'output' keys
        save_path: str, path to save the figure. if None, show the figure
        task_id: str, task id for title
        """
        nrows, ncols = 2, max(5, len(train))
        fig = plt.figure()
        # grids_io = [(input, output), ...]
        for i, gs in enumerate(train):
            ax = fig.add_subplot(nrows, ncols, i+1)
            ax.pcolormesh(
                gs['input'], edgecolors=s.process.colors[-1], linewidth=0.5, cmap=s.process.colormap, vmin=0, vmax=10)
            ax.invert_yaxis()
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title(f'Input {i+1}')
            ax = fig.add_subplot(nrows, ncols, i+1+ncols)
            ax.pcolormesh(
                gs['output'], edgecolors=s.process.colors[-1], linewidth=0.5, cmap=s.process.colormap, vmin=0, vmax=10)
            ax.invert_yaxis()
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title(f'Output {i+1}')
        fig.tight_layout()
        if task_id:
            fig.suptitle(f'Task {task_id}')
        else:
            fig.suptitle('A task :)')
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
    def show_task(tasks, save_path=None, task_id=None):
        """
        Show the input-output pair of a training task
        tasks: dict, contains 'train' and 'test' keys, each key contains a list of dict
        save_path: str, path to save the figure. if None, show the figure
        task_id: str, task id for title
        """
        nrows, ncols = 4, max(5, len(tasks['train']))
        train = tasks['train']
        test = tasks['test']

        fig = plt.figure()
        # grids_io = [(input, output), ...]
        for i, gs in enumerate(train):
            ax = fig.add_subplot(nrows, ncols, i+1)
            ax.pcolormesh(
                gs['input'], edgecolors=colors[-1], linewidth=0.5, cmap=colormap, vmin=0, vmax=10)
            ax.invert_yaxis()
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title(f'Input {i+1}')
            ax = fig.add_subplot(nrows, ncols, i+1+ncols)
            ax.pcolormesh(
                gs['output'], edgecolors=colors[-1], linewidth=0.5, cmap=colormap, vmin=0, vmax=10)
            ax.invert_yaxis()
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title(f'Output {i+1}')

        for i, gs in enumerate(test):
            ax = fig.add_subplot(nrows, ncols, i+1+2*ncols)
            ax.pcolormesh(
                gs['input'], edgecolors=colors[-1], linewidth=0.5, cmap=colormap, vmin=0, vmax=10)
            ax.invert_yaxis()
            ax.set_aspect('equal')
            ax.axis('off')
            ax.set_title(f'Test Input {i+1}')

        if task_id:
            fig.suptitle(f'Task {task_id}')
        else:
            fig.suptitle('A task :)')
        fig.tight_layout()
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
    def load():
        import json
        s.process.data = json.loads(File.getFileContent(s.process.fileLoc))
    s = ObjMaker.variablesAndFunction(locals())
    return s
def ARCViewer():
    from timeline.t2024.ui_lib.IpyComponents import Utils, IpywidgetsComponentsEnum, ComponentsLib
    showAllBtn = Utils.get_comp({"description":"showAllKeys"}, IpywidgetsComponentsEnum.Button, className = "w-fit")
    keyField = Utils.get_comp({"placeholder":"enter key"}, IpywidgetsComponentsEnum.Text, bind=False)
    plotBtn = Utils.get_comp({"description":"plot"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    copyToVarBtn = Utils.get_comp({"description":"assign to res var"}, IpywidgetsComponentsEnum.Button, className = "w-auto")
    outArea = Utils.get_comp({}, ComponentsLib.CustomOutput)
    rowOutput = Utils.get_comp({}, ComponentsLib.CustomOutput)
    container = Utils.container([Utils.container([keyField,plotBtn, showAllBtn, copyToVarBtn,rowOutput]), outArea], className="flex flex-column")
    model = PlotterModel()
    spaceToCopy = {}
    def onPlot(w):
        key = s.views.keyField.outputs.layout.value.strip()
        if key == "":
            return 
        s.views.outArea.state.controller.clear()
        with s.views.outArea.state.controller._out:
            s.process.model.handlers.show_task(s.process.model.process.data[key], task_id=key)
    def onShowAllkeys(w):
        s.views.outArea.state.controller.clear()
        with s.views.outArea.state.controller._out:
            print(str(list(s.process.model.process.data.keys())))
    def onAssign(w):
        key = s.views.keyField.outputs.layout.value.strip()
        if key == "":
            return 
        data = s.process.model.process.data[key]
        s.process.spaceToCopy["res"] = data
        s.views.rowOutput.state.controller.clear()
        for i, inp in enumerate(data["train"]):
            s.process.spaceToCopy["train" + str(i+1) + "_in"] = inp["input"]
            s.process.spaceToCopy["train" + str(i+1) + "_out"] = inp["output"]
        with s.views.rowOutput.state.controller._out:
            print("copied to 'res'. Also train vars")
    showAllBtn.handlers.handle = onShowAllkeys
    plotBtn.handlers.handle = onPlot
    copyToVarBtn.handlers.handle = onAssign
    s = ObjMaker.uisOrganize(locals())
    return s
class Main:
    def viewer():
        arcViewer = ARCViewer()
        arcViewer.process.model.handlers.load()
        return arcViewer