"""Launch with: python main.py (Python 3.10+, standard library only)."""
import tkinter as tk
from tkinter import ttk
from tree_model import build_values, build_expression, traversals, evaluate, number, format_number

CREAM='#f5efe6'; INK='#262824'; BLUE='#2999ed'; GREEN='#009b79'; GOLD='#e6b836'; CORAL='#f37360'

class TreeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tree Studio • Traversal Explorer')
        self.geometry('1280x830'); self.minsize(1020,740); self.configure(bg=CREAM)
        self.root_node=None; self.orders={}; self.positions={}; self.scale=1; self.offset=[0,0]
        self.highlight=None; self.job=None; self.sequence=[]; self.step_index=0
        self.kind=tk.StringVar(value='Numerical'); self.layout=tk.StringVar(value='Binary search tree')
        self.expression=tk.BooleanVar(); self.notation=tk.StringVar(value='Infix'); self.order=tk.StringVar(value='Preorder')
        self.status=tk.StringVar(value='Ready. Build a tree to begin.'); self.result=tk.StringVar(value='Overall value  —')
        self.inputs=tk.StringVar(); self.output_vars={}
        style=ttk.Style(self); style.theme_use('clam')
        style.configure('TCombobox',padding=7)
        header=tk.Frame(self,bg=CREAM); header.pack(fill='x',padx=25,pady=(20,15))
        tk.Label(header,text='TREE STUDIO',font=('Segoe UI',24,'bold'),bg=CREAM,fg=INK).pack(side='left')
        tk.Label(header,text='BUILD  /  EXPLORE  /  UNDERSTAND',font=('Segoe UI',10),bg=CREAM,fg='#77776f').pack(side='right')
        body=tk.Frame(self,bg=CREAM); body.pack(fill='both',expand=True,padx=24)
        side=tk.Frame(body,bg=CREAM,width=285); side.pack(side='left',fill='y',padx=(0,18)); side.pack_propagate(False)
        self.label(side,'01   Build your tree',16,True)
        self.label(side,'Value type')
        self.combo(side,self.kind,['Numerical','Alphabetical'],self.mode_changed)
        self.label(side,'Tree arrangement')
        self.layout_combo=self.combo(side,self.layout,['Binary search tree','Level-filled tree'])
        self.check=tk.Checkbutton(side,text='Include arithmetic operators',variable=self.expression,command=self.mode_changed,bg=CREAM,activebackground=CREAM,font=('Segoe UI',11))
        self.check.pack(anchor='w',pady=(14,5))
        self.label(side,'Expression notation')
        self.notation_combo=self.combo(side,self.notation,['Infix','Prefix','Postfix'])
        self.label(side,'Values / expression')
        self.entry=tk.Entry(side,textvariable=self.inputs,font=('Segoe UI',12),bg='white',relief='solid',bd=1)
        self.entry.pack(fill='x',ipady=10,pady=(0,7)); self.entry.bind('<Return>',lambda e:self.build())
        self.hint=tk.Label(side,text='',bg=CREAM,fg='#66665e',wraplength=275,justify='left',font=('Segoe UI',10)); self.hint.pack(fill='x')
        self.button(side,'Build tree  →',self.build,BLUE).pack(fill='x',pady=(18,8))
        self.button(side,'Load example',self.example,GOLD).pack(fill='x',pady=4)
        self.button(side,'Clear workspace',self.clear,CORAL).pack(fill='x',pady=4)
        self.label(side,'02   Walk the branches',16,True)
        self.combo(side,self.order,['Preorder','Inorder','Postorder','Level order'],self.reset_walk)
        row=tk.Frame(side,bg=CREAM); row.pack(fill='x',pady=10)
        for name,fn in [('Play',self.play),('Step',self.step),('Pause',self.pause)]: self.button(row,name,fn,GREEN).pack(side='left',expand=True,fill='x',padx=2)
        self.label(side,'Click a node to inspect it.\nDrag the graph to move.\nScroll to zoom at your pointer.',10)
        right=tk.Frame(body,bg=CREAM); right.pack(side='left',fill='both',expand=True)
        top=tk.Frame(right,bg=CREAM); top.pack(fill='x',pady=(0,10))
        tk.Label(top,text='Tree canvas',bg=CREAM,font=('Segoe UI',16,'bold')).pack(side='left')
        for title,fn in [('−',lambda:self.zoom(.8)),('+',lambda:self.zoom(1.25)),('Fit',self.fit),('←',lambda:self.pan(50,0)),('→',lambda:self.pan(-50,0)),('↑',lambda:self.pan(0,50)),('↓',lambda:self.pan(0,-50))]:
            self.button(top,title,fn,CREAM).pack(side='right',padx=2)
        self.canvas=tk.Canvas(right,bg='#1d252b',highlightthickness=1,highlightbackground=INK,height=380)
        self.canvas.pack(fill='both',expand=True)
        self.canvas.bind('<Configure>',lambda e:self.draw())
        self.canvas.bind('<ButtonPress-1>',self.drag_start); self.canvas.bind('<B1-Motion>',self.drag)
        self.canvas.bind('<MouseWheel>',lambda e:self.zoom(1.15 if e.delta>0 else 1/1.15,e.x,e.y))
        self.canvas.bind('<Button-4>',lambda e:self.zoom(1.15,e.x,e.y)); self.canvas.bind('<Button-5>',lambda e:self.zoom(1/1.15,e.x,e.y))
        tk.Label(right,textvariable=self.result,bg=CREAM,fg=GREEN,font=('Segoe UI',14,'bold'),anchor='w').pack(fill='x',pady=10)
        for name,color in zip(['Preorder','Inorder','Postorder','Level order'],[GOLD,GREEN,CORAL,BLUE]):
            frame=tk.Frame(right,bg=color,highlightbackground=INK,highlightthickness=1); frame.pack(fill='x',pady=3)
            self.button(frame,name,lambda n=name:self.select_order(n),color).pack(side='left',padx=4)
            var=tk.StringVar(value='—'); self.output_vars[name]=var
            entry=tk.Entry(frame,textvariable=var,state='readonly',readonlybackground=color,fg=INK,relief='flat',font=('Consolas',11))
            entry.pack(side='left',fill='x',expand=True,padx=10,ipady=10)
        tk.Label(self,textvariable=self.status,bg=CREAM,fg=INK,anchor='w',font=('Segoe UI',10),wraplength=1200).pack(fill='x',padx=25,pady=12)
        self.mode_changed()

    def label(self,parent,text,size=11,bold=False):
        tk.Label(parent,text=text,bg=CREAM,fg=INK,font=('Segoe UI',size,'bold' if bold else 'normal'),justify='left').pack(anchor='w',pady=(13,7))
    def button(self,parent,text,command,color):
        return tk.Button(parent,text=text,command=command,bg=color,fg=INK,activebackground='#fff5d7',relief='solid',bd=1,cursor='hand2',font=('Segoe UI',10,'bold'),padx=10,pady=7)
    def combo(self,parent,var,values,callback=None):
        box=ttk.Combobox(parent,textvariable=var,values=values,state='readonly'); box.pack(fill='x')
        if callback: box.bind('<<ComboboxSelected>>',lambda e:callback())
        return box
    def mode_changed(self):
        alpha=self.kind.get()=='Alphabetical'
        if alpha:self.expression.set(False)
        self.check.configure(state='disabled' if alpha else 'normal')
        expr=self.expression.get()
        self.notation_combo.configure(state='readonly' if expr else 'disabled')
        self.layout_combo.configure(state='disabled' if expr else 'readonly')
        self.hint.configure(text=('Infix: (8 + 4) * 3\nPrefix: * + 8 4 3\nPostfix: 8 4 + 3 *' if expr else 'Separate values with commas or spaces.\nExamples: 8 4 12 2 6 10 14' if not alpha else 'Separate letters or words with spaces.\nExample: M F T B H R Z'))
    def build(self):
        try:
            expr=self.expression.get()
            root=build_expression(self.inputs.get(),self.notation.get()) if expr else build_values(self.inputs.get(),self.kind.get(),self.layout.get())
            orders=traversals(root)
            result=('Expression value  =  '+format_number(evaluate(root)) if expr else 'Sum of all numbers  =  '+format_number(sum(number(n.value) for n in orders['Preorder'])) if self.kind.get()=='Numerical' else 'Alphabetical tree  •  '+str(len(orders['Preorder']))+' nodes')
        except (ValueError,RecursionError) as error:
            self.status.set('Cannot build: '+str(error)); return
        self.reset_walk(); self.root_node=root; self.orders=orders; self.result.set(result)
        for name,nodes in orders.items():self.output_vars[name].set(' → '.join(n.value for n in nodes))
        self.positions={}; index=0
        def place(node,depth):
            nonlocal index
            if not node:return
            place(node.left,depth+1); self.positions[node]=(index*100,depth*110); index+=1; place(node.right,depth+1)
        place(root,0); self.fit()
        self.status.set('Tree built. Traversals visit the same nodes in different orders; the sum stays the same.' if not expr else 'Expression evaluated using the tree structure. Inorder output omits parentheses; it is a traversal, not a new formula.')
    def example(self):
        self.inputs.set(('(8 + 4) * (10 - 7)' if self.notation.get()=='Infix' else '* + 8 4 - 10 7' if self.notation.get()=='Prefix' else '8 4 + 10 7 - *') if self.expression.get() else 'M F T B H R Z' if self.kind.get()=='Alphabetical' else '8 4 12 2 6 10 14'); self.build()
    def clear(self):
        self.reset_walk(); self.root_node=None; self.orders={}; self.positions={}; self.inputs.set(''); self.result.set('Overall value  —')
        for var in self.output_vars.values():var.set('—')
        self.status.set('Workspace cleared.'); self.draw()
    def fit(self):
        if not self.positions:self.draw();return
        self.update_idletasks(); coords=list(self.positions.values()); xs=[p[0] for p in coords]; ys=[p[1] for p in coords]
        w,h=self.canvas.winfo_width(),self.canvas.winfo_height()
        self.scale=max(.08,min(1.3,(w-90)/(max(xs)-min(xs)+80),(h-90)/(max(ys)-min(ys)+80)))
        self.offset=[w/2-(max(xs)+min(xs))/2*self.scale,h/2-(max(ys)+min(ys))/2*self.scale];self.draw()
    def zoom(self,factor,x=None,y=None):
        x=self.canvas.winfo_width()/2 if x is None else x;y=self.canvas.winfo_height()/2 if y is None else y
        new=max(.08,min(3,self.scale*factor));ratio=new/self.scale
        self.offset=[x+(self.offset[0]-x)*ratio,y+(self.offset[1]-y)*ratio];self.scale=new;self.draw()
    def pan(self,x,y):self.offset[0]+=x;self.offset[1]+=y;self.draw()
    def drag_start(self,event):
        self.last=(event.x,event.y)
        for node,(x,y) in self.positions.items():
            if (event.x-x*self.scale-self.offset[0])**2+(event.y-y*self.scale-self.offset[1])**2 <= (28*self.scale)**2:
                self.highlight=node;self.status.set('Selected node: '+node.value);self.draw();break
    def drag(self,event):
        x,y=self.last;self.pan(event.x-x,event.y-y);self.last=(event.x,event.y)
    def draw(self):
        c=self.canvas;c.delete('all');w,h=c.winfo_width(),c.winfo_height()
        for x in range(20,w,40):
            for y in range(20,h,40):c.create_oval(x,y,x+1,y+1,fill='#354047',outline='')
        if not self.positions:
            c.create_text(w/2,h/2-12,text='Your next idea starts with a root.',fill='#eee8dd',font=('Segoe UI',19,'bold'))
            c.create_text(w/2,h/2+22,text='Enter values, then choose Build tree.',fill='#a0afb5',font=('Segoe UI',11));return
        def point(n):
            x,y=self.positions[n];return x*self.scale+self.offset[0],y*self.scale+self.offset[1]
        for n in self.positions:
            x,y=point(n)
            for child in (n.left,n.right):
                if child:
                    xx,yy=point(child);c.create_line(x,y,xx,yy,fill='#344b50',width=max(2,7*self.scale));c.create_line(x,y,xx,yy,fill='#c0d2d1',width=max(1,2*self.scale))
        for n in self.positions:
            x,y=point(n);r=27*self.scale;color=GOLD if n is self.highlight else GREEN if n is self.root_node else BLUE
            c.create_oval(x-r-5,y-r-5,x+r+5,y+r+5,outline=color,width=1)
            c.create_oval(x-r,y-r,x+r,y+r,fill='#23343b',outline=color,width=max(1,3*self.scale))
            c.create_text(x,y,text=n.value,fill='#fff5df',font=('Segoe UI',max(6,int(12*self.scale)),'bold'))
        c.create_text(14,16,text=f'{len(self.positions)} NODES  •  {self.scale:.0%}',anchor='w',fill='#a0afb5',font=('Segoe UI',9))
    def pause(self):
        if self.job:self.after_cancel(self.job);self.job=None
    def reset_walk(self):
        self.pause();self.step_index=0;self.highlight=None;self.draw() if hasattr(self,'canvas') else None
    def select_order(self,name):self.order.set(name);self.reset_walk();self.step()
    def step(self):
        self.pause();nodes=self.orders.get(self.order.get(),[])
        if not nodes:self.status.set('Build a tree before starting a traversal.');return False
        if self.step_index>=len(nodes):self.step_index=0
        self.highlight=nodes[self.step_index];self.step_index+=1
        self.status.set(f'{self.order.get()} • Step {self.step_index}/{len(nodes)} • '+ ' → '.join(n.value for n in nodes[:self.step_index]));self.draw()
        return self.step_index<len(nodes)
    def play(self):
        if self.step():self.job=self.after(650,self.play)

if __name__=='__main__':TreeApp().mainloop()
