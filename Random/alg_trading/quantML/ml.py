def result_report(res, threshold=0.01, verbose=False):
    if verbose:
        print(f'Average Weekly Return {res.actual.mean()*100:.2f}')
        print(f'Weekly Return on Threshold {res[res.prediction >= threshold].actual.mean()*100:.2f}')
