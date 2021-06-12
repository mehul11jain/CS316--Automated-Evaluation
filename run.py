#!/usr/bin/python
import glob, sys, tarfile, subprocess, os, csv
class Evaluate:
    def __init__(self, asgn, args):
        
        self.assignment = asgn
        self.group = "unknown"
        self.dir = os.getcwd()
        self.result = {}
        self.check_error = False
        self.check_rtl = False
        self.check_tac = False
        self.check_tokens = False
        self.check_ast = False        
        self.process_cmd_options(args)
        self.f = open("./Evaluation_Logs/Evaluation_log_"+ self.group + ".log", "w")
        self.extract_submission()
        self.evaluate()
        self.writeResults()
        self.f.close()
    
    def writeResults(self):
        
        # clean up
        subprocess.run(["rm", "-rf", "sclp"],stderr=self.f, stdout=self.f)
        for j in ["toks", "ast", "tac", "rtl"]:
            for i in glob.glob("./NonError/*."+j):
                subprocess.run(["rm", i], stderr=self.f, stdout=self.f) 
        
        with open("./CSV/" + self.assignment+"-Evaluation.csv", "a") as file:
            writer = csv.writer(file)
            header = ["Group No.", "compilation error"]   
            if os.path.getsize("./CSV/"+self.assignment+"-Evaluation.csv") == 0:         
                for j in ["tokens", "ast", "tac", "rtl", "error"]:
                    if j in self.result.keys():
                        for t in self.result[j].keys():
                            header.append(j+"::"+t)
                writer.writerow(header)

            files = glob.glob("./NonError/*.c")            
            row=[self.group]
            row.append(self.result["compilation error"])
            for i in range(1, len(files)+1):
                if self.check_tokens:
                    row.append(self.result["tokens"]["test"+str(i)])
            for i in range(1, len(files)+1):    
                if self.check_ast:
                    row.append(self.result["ast"]["test"+str(i)])
            for i in range(1, len(files)+1):
                if self.check_tac:
                    row.append(self.result["tac"]["test"+str(i)])
            for i in range(1, len(files)+1):
                if self.check_rtl:
                    row.append(self.result["rtl"]["test"+str(i)])
            for i in range(1, len(files)+1):
                if self.check_error:
                    row.append(self.result["error"]["test"+str(i)])
            writer.writerow(row);
            file.close()


    def evaluate(self):
        if self.check_tokens:
            self.eval_tokens()
        if self.check_ast:
            self.eval_ast()
        if self.check_tac:
            self.eval_tac()
        if self.check_rtl:
            self.eval_rtl();
        if self.check_error:
            self.eval_error();

    def extract_submission(self):
        file = tarfile.open("./"+self.assignment + "/" + self.group + ".tar.gz")
        file.extractall(self.assignment)
        file.close()
        self.build_project()
    
    def build_project(self):
        path = "./" + self.assignment + "/" + self.group + "/"
        os.chdir(path)
        
        status = subprocess.run("make", stdout= self.f,stderr= self.f)        
        if status.returncode != 0:
            self.result["compilation error"] = "yes"
            for keys in self.result.keys():
                if keys == "compilation error" or keys == "Group No.":
                    continue;
                else:
                    for i in self.result[keys].keys():
                        self.result[keys][i] = "fail"
            os.chdir(self.dir)
            self.writeResults()
            exit(1)
        else: 
            self.result["compilation error"] = "no"
        subprocess.run(["mv", "sclp" , self.dir], stdout= self.f, stderr=self.f)
        os.chdir(self.dir)
        subprocess.run(["rm", "-r", "./"+self.assignment + "/" + self.group],stdout=self.f, stderr=self.f)
        


    def process_cmd_options(self, args):
        files = glob.glob("./NonError/*.c")
        for i in args:            
            if i == "-tac":
                self.check_tac = True
                self.result["tac"] = {}
                for i in range(1, len(files)+1):
                    self.result["tac"]["test"+str(i)] = {};
            elif i == "-tokens":
                self.check_tokens = True
                self.result["tokens"] = {}
                for i in range(1, len(files)+1):
                    self.result["tokens"]["test"+str(i)] = {} ;
            elif i == "-ast":
                self.check_ast = True
                self.result["ast"] = {}
                for i in range(1, len(files)+1):
                    self.result["ast"]["test"+str(i)] = {};
            elif i == "-error":
                self.check_error = True
                self.result["error"] = {}
                for i in range(1, len(files)+1):
                    self.result["error"]["test"+str(i)] = {};
            elif i == "-rtl":
                self.check_rtl = True
                self.result["rtl"] = {}
                for i in range(1, len(files)+1):
                    self.result["rtl"]["test"+str(i)] = {};
            elif "group" in i:
                self.group = i

    
    def eval_tac(self):
        if self.check_tac is True:
            files = glob.glob("./NonError/*.c")
            for file in files:
                subprocess.run(["./sclp", file, "-tac", "-sa-tac"], stderr=self.f, stdout=self.f)
                # subprocess.run(["diff", "-Bw", "-N", "./expected_op"])
            for i in range(1, len(files)+1):                
                f = open("temp2.txt", "w")
                subprocess.run(["diff", "-B", "-w", "-N", "./NonError/expected_op_tac" + str(i)+".txt",  "./NonError/test"+ str(i) + ".c.tac"], stdout=f)                
                f.close()
                if(os.path.getsize("temp2.txt") > 0):
                    self.result["tac"]["test"+str(i)] = "Fail";
                else:
                    self.result["tac"]["test"+str(i)] = "Pass";
                subprocess.run(["rm", "-r", "temp2.txt"], stdout=self.f, stderr=self.f)

    def eval_ast(self):
        if self.check_ast is True:
            files = glob.glob("./NonError/*.c")
            for file in files:
                subprocess.run(["./sclp", file, "-ast", "-sa-ast"], stdout=self.f, stderr=self.f)
                # subprocess.run(["diff", "-Bw", "-N", "./expected_op"])
            for i in range(1, len(files)+1):                
                f = open("temp2.txt", "w")
                subprocess.run(["diff", "-B", "-w", "-N", "./NonError/expected_op_ast" + str(i)+".txt",  "./NonError/test"+ str(i) + ".c.ast"], stdout=f)                
                f.close()
                if(os.path.getsize("temp2.txt") > 0):
                    self.result["ast"]["test"+str(i)] = "Fail";
                else:
                    self.result["ast"]["test"+str(i)] = "Pass";
                subprocess.run(["rm", "-r", "temp2.txt"], stderr=self.f, stdout=self.f)

    def eval_tokens(self):
        if self.check_tokens is True:
            files = glob.glob("./NonError/*.c")
            for file in files:
                subprocess.run(["./sclp", file, "-tokens", "-sa-scan"],stderr=self.f, stdout=self.f)
                # subprocess.run(["diff", "-Bw", "-N", "./expected_op"])
            for i in range(1, len(files)+1):                
                f = open("temp2.txt", "w")
                subprocess.run(["diff", "-B", "-w", "-N", "./NonError/expected_op_token" + str(i)+".txt",  "./NonError/test"+ str(i) + ".c.toks"], stdout=f)                
                f.close()
                if(os.path.getsize("temp2.txt") > 0):
                    self.result["tokens"]["test"+str(i)] = "Fail";
                else:
                    self.result["tokens"]["test"+str(i)] = "Pass";
                subprocess.run(["rm", "-r", "temp2.txt"],stderr=self.f, stdout=self.f)

    def eval_rtl(self):
        if self.check_rtl is True:
            files = glob.glob("./NonError/*.c")
            for file in files:
                subprocess.run(["./sclp", file, "-rtl", "-sa-rtl"],stderr=self.f, stdout=self.f)
                # subprocess.run(["diff", "-Bw", "-N", "./expected_op"])
            for i in range(1, len(files)+1):                
                f = open("temp2.txt", "w")
                subprocess.run(["diff", "-B", "-w", "-N", "./NonError/expected_op_rtl" + str(i)+".txt",  "./NonError/test"+ str(i) + ".c.rtl"], stdout=f)                
                f.close()
                if(os.path.getsize("temp2.txt") > 0):
                    self.result["rtl"]["test"+str(i)] = "Fail";
                else:
                    self.result["rtl"]["test"+str(i)] = "Pass";
                subprocess.run(["rm", "-r", "temp2.txt"], stderr=self.f, stdout=self.f)
    
    def eval_error(self):
        if self.check_error is True:
            files = glob.glob("./Error/*.c")                            
            for i in range(1, len(files)+1):                
                exec = subprocess.Popen(["./sclp", "./Error/test"+str(i)+".c"], stdout=subprocess.PIPE, stderr=self.f)
                data = exec.communicate()[0]
                
                if(exec.returncode != 0):
                    self.result["error"]["test"+str(i)] = "Pass";
                else:
                    self.result["error"]["test"+str(i)] = "Fail";                        
            

Ev = Evaluate("A1", sys.argv)


