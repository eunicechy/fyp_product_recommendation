import os 
import sys 
import click
# from app import create_app, db

COV = None
if os.environ.get('FLASK_COVERAGE'):    
  import coverage    
  COV = coverage.coverage(
    data_file=os.path.join(os.path.dirname(__file__), '.coverage'),
    branch=True, 
    include='app/*'
  )  
  COV.start()

#### if main use this
# app = create_app(os.getenv('FLASK_CONFIG') or 'default')

from app import app ####THIS

@app.cli.command() 
@click.option('--coverage/--no-coverage', default=False, help='Run tests under code coverage.') 
def test(coverage):    
  """Run the unit tests."""    
  if coverage and not os.environ.get('FLASK_COVERAGE'):        
    os.environ['FLASK_COVERAGE'] = '1'        
    os.execvp(sys.executable, [sys.executable] + sys.argv)    
    import unittest    
    tests = unittest.TestLoader().discover('tests')    
    unittest.TextTestRunner(verbosity=2).run(tests)
    # unittest.main()    
    if COV:        
      COV.stop()        
      COV.save()        
      print('Coverage Summary:')        
      COV.report()        
      basedir = os.path.abspath(os.path.dirname(__file__))        
      covdir = os.path.join(basedir, 'tmp/coverage')        
      COV.html_report(directory=covdir)        
      print('HTML version: file://%s/index.html' % covdir)        
      COV.erase() 