# SBM4C-C-
Simple Build Manager for C and C++

## requirements
  - gcc / g++ in path
  - the ability to read
    
## stage of the project
- implemented:
  - executable building
  - new, clean, build, rebuild options
- not implemented yet:
  - building to object files
  - building to libraries (linux .lib and windows .dll)
  - building to gnu assembly
  - relations

## usage
1. creating a new project  
   type `sbm new <project_path>` and finish the setup  
   <img width="743" height="244" alt="image" src="https://github.com/user-attachments/assets/916e1c10-f7d4-46f6-983e-5d9bbf08108d" />  
2. building a project  
   type `sbm build <project_path>`  
   <img width="956" height="264" alt="image" src="https://github.com/user-attachments/assets/cd43a50f-44bb-433d-9af2-c5584041b6b2" />  
3. cleaning a project  
   type `sbm clean <project_path>`  
   <img width="368" height="82" alt="image" src="https://github.com/user-attachments/assets/153f034f-0480-4f0c-9209-de764ac690af" />  
4. rebuilding a project  
   type `sbm rebuild <project_path>` (its just clean + build)  

## configuring
Depending on your inputs in creating the project by default you will have a `__sbmconfig__` looking something like this  
```ini
[compiler]
compiler = gcc
standard = c89
output = dist/output.exe
flags = 
```
NOTE:
- `compiler` should be either `gcc` or `g++`
- `standard` should be a valid standard for the compiler
- `output` is the path of the result  
  based on the extenstion the file will be built as either executable (linux: `.out`, windows: `.exe`), asm (`.s`, `.asm`), object (linux: `.o`, windows: `.obj`) or library (linux: `.lib`, windows: `.dll`)

1. Adding flags for a specific module
   to your config add:
   ```ini
   [m_<module_name>]
   flags = <flags>
   ```
   example for module `main`:
   ```ini
   [m_main]
   flags = -O2
   ```
