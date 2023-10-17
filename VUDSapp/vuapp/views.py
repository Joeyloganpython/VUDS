from re import I
from unittest import result
from django.shortcuts import render, redirect, get_object_or_404
from vuapp.forms import FlowSheetForm, TextfileUploadForm, DicomfileUploadForm
from vuapp.random_forest_flowsheet import RandomForestFlowSheet
from vuapp.txtfilepred import NN_by_pressure
from vuapp.dicom_pred import Dicom_pred


def index(request):
    return render(request, "vuapp/index.html")


def new_flowsheet(request):
    form = FlowSheetForm

    if request.method == "POST":
        form = FlowSheetForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            print(form.cleaned_data)
            rf = RandomForestFlowSheet(cleaned_data=form.cleaned_data)
            pred = rf.make_predictions()
            print(pred)
            request.session["prediction"] = pred

            return redirect("flow_result")
            # return index(request)
        else:
            print("Error form invalid")
    return render(request, "vuapp/new_flowsheet.html", {"form": form})


def flow_result(request):
    return render(
        request, "vuapp/flow_result.html", {"result": request.session["prediction"]}
    )


def upload_text_file(request):
    if request.method == "POST":
        form = TextfileUploadForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save()
            txtfile = request.FILES["upload"]
            print(txtfile)
            model = NN_by_pressure(
                txtfile=txtfile, ebc=form.cleaned_data["expected_bladder_capacity"]
            )
            result, pabd_plot, time_plot = model.make_predictions()
            request.session["text_prediction"] = result
            request.session["padb_plot"] = pabd_plot
            request.session["time_plot"] = time_plot
            return redirect("textfileresult")
    else:
        form = TextfileUploadForm()
    return render(request, "vuapp/upload_text_file.html", {"form": form})


def textfileresult(request):
    return render(
        request,
        "vuapp/textfileresult.html",
        {
            "result": request.session["text_prediction"],
            "pabd_plot": request.session["padb_plot"],
            "time_plot": request.session["time_plot"],
        },
    )


def upload_dicom_file(request):
    if request.method == "POST":
        form = DicomfileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            dicom_file = request.FILES["dicom_upload"]
            model = Dicom_pred(dicom_file=dicom_file)
            dicomviz, okmessage = model.pred_ultrasound()
            if okmessage == "Good_Image":
                request.session["dicom_viz"] = dicomviz
                print(dicomviz)
                return redirect("dicomresult")
    else:
        form = DicomfileUploadForm()
    return render(request, "vuapp/upload_dicom_file.html", {"form": form})


def dicomresult(request):
    return render(
        request,
        "vuapp/dicomresult.html",
        {"dicomviz": request.session["dicom_viz"]},
    )
