"""P14 Matplotlib pre-frozen *visible* behavioral tests.

Original public problem: the AxLine setters need a single xy-pair argument.
These tests are NOT SWE-bench-Live gold/test_patch or a hidden task oracle.
Created before any P14 candidate, with the original source base SHA frozen.
Run with the historic matplotlib checkout installed in the test runner.
"""
import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
import pytest


def test_single_xy_pair_positional_setters():
    fig, ax = plt.subplots()
    try:
        line = ax.axline((0.0, 0.0), (1.0, 1.0))
        line.set_xy1((0.2, 0.3))
        line.set_xy2((0.7, 0.8))
        assert line.get_xy1() == (0.2, 0.3)
        assert line.get_xy2() == (0.7, 0.8)
    finally:
        plt.close(fig)


def test_backwards_compatible_two_scalars():
    fig, ax = plt.subplots()
    try:
        line = ax.axline((0.0, 0.0), (1.0, 1.0))
        line.set_xy1(0.25, 0.35)
        line.set_xy2(0.75, 0.85)
        assert line.get_xy1() == (0.25, 0.35)
        assert line.get_xy2() == (0.75, 0.85)
    finally:
        plt.close(fig)


def test_artist_batch_set_xy_properties():
    fig, ax = plt.subplots()
    try:
        line = ax.axline((0.0, 0.0), (1.0, 1.0))
        line.set(xy1=(0.3, 0.4), xy2=(0.6, 0.7))
        assert line.get_xy1() == (0.3, 0.4)
        assert line.get_xy2() == (0.6, 0.7)
    finally:
        plt.close(fig)


def test_xy_keyword_signature_for_each_setter():
    fig, ax = plt.subplots()
    try:
        line = ax.axline((0.0, 0.0), (1.0, 1.0))
        line.set_xy1(xy=(0.15, 0.25))
        line.set_xy2(xy=(0.65, 0.75))
        assert line.get_xy1() == (0.15, 0.25)
        assert line.get_xy2() == (0.65, 0.75)
    finally:
        plt.close(fig)


def test_slope_mode_rejects_second_xy_pair():
    fig, ax = plt.subplots()
    try:
        line = ax.axline((0.0, 0.0), slope=0.5)
        line.set_xy1((0.3, 0.4))
        assert line.get_xy1() == (0.3, 0.4)
        with pytest.raises(ValueError, match="Cannot set an 'xy2'"):
            line.set_xy2((0.6, 0.8))
    finally:
        plt.close(fig)


def test_render_after_xy_updates():
    fig, ax = plt.subplots()
    try:
        line = ax.axline((0.0, 0.0), (1.0, 1.0))
        line.set_xy1((0.2, 0.3))
        line.set_xy2((0.7, 0.8))
        fig.canvas.draw()
        assert line.get_transform() is not None
    finally:
        plt.close(fig)
